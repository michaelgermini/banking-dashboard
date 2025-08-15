from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd


@dataclass
class ScenarioConfig:
    name: str
    revenue_growth_annual: float
    deposit_growth_annual: float
    aum_growth_annual: float
    margin_pct: float
    volatility_pct: float
    npl_base_pct: float
    var_base_bps: float
    lcr_base_pct: float


SCENARIOS: Dict[str, ScenarioConfig] = {
    "Baseline": ScenarioConfig(
        name="Baseline",
        revenue_growth_annual=0.05,
        deposit_growth_annual=0.04,
        aum_growth_annual=0.06,
        margin_pct=0.32,
        volatility_pct=0.06,
        npl_base_pct=1.8,
        var_base_bps=85.0,
        lcr_base_pct=135.0,
    ),
    "Adverse": ScenarioConfig(
        name="Adverse",
        revenue_growth_annual=0.01,
        deposit_growth_annual=0.00,
        aum_growth_annual=0.01,
        margin_pct=0.28,
        volatility_pct=0.12,
        npl_base_pct=3.2,
        var_base_bps=130.0,
        lcr_base_pct=115.0,
    ),
    "Severe": ScenarioConfig(
        name="Severe",
        revenue_growth_annual=-0.03,
        deposit_growth_annual=-0.02,
        aum_growth_annual=-0.04,
        margin_pct=0.24,
        volatility_pct=0.18,
        npl_base_pct=5.2,
        var_base_bps=180.0,
        lcr_base_pct=95.0,
    ),
}


def month_range(periods: int, end: dt.date | None = None) -> pd.DatetimeIndex:
    if end is None:
        end = dt.date.today().replace(day=1)
    end_ts = pd.Timestamp(end)
    return pd.date_range(end=end_ts, periods=periods, freq="MS")


def generate_financial_data(
    periods: int = 36,
    scenario: str = "Baseline",
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    cfg = SCENARIOS.get(scenario, SCENARIOS["Baseline"])

    dates = month_range(periods)
    months = np.arange(periods)

    def annual_to_monthly(g: float) -> float:
        return (1.0 + g) ** (1.0 / 12.0) - 1.0

    revenue_growth_m = annual_to_monthly(cfg.revenue_growth_annual)
    deposits_growth_m = annual_to_monthly(cfg.deposit_growth_annual)
    aum_growth_m = annual_to_monthly(cfg.aum_growth_annual)

    revenue0 = 120.0  # CHF m per month
    deposits0 = 8000.0  # CHF m
    aum0 = 15000.0  # CHF m

    # Core time series with trend + noise
    revenue = revenue0 * (1 + revenue_growth_m) ** months * (
        1 + rng.normal(0, cfg.volatility_pct, size=periods)
    )
    margin_pct = np.clip(
        rng.normal(cfg.margin_pct, cfg.volatility_pct / 4.0, size=periods), 0.15, 0.45
    )
    gross_margin = revenue * margin_pct

    deposits = deposits0 * (1 + deposits_growth_m) ** months
    deposits = deposits * (1 + rng.normal(0, cfg.volatility_pct / 4.0, size=periods))
    deposits_growth = np.r_[np.nan, np.diff(deposits)] / np.r_[np.nan, deposits[:-1]] * 100.0

    aum = aum0 * (1 + aum_growth_m) ** months
    aum = aum * (1 + rng.normal(0, cfg.volatility_pct / 3.0, size=periods))

    # Segment profitability decomposition (Retail, Private, Corporate)
    segment_shares = np.clip(
        rng.dirichlet(alpha=[2.5, 2.0, 1.5], size=periods), 0.1, 0.8
    )
    segment_shares = segment_shares / segment_shares.sum(axis=1, keepdims=True)
    profit_total = gross_margin * 0.65  # assume 65% of gross margin becomes operating profit
    profit_retail = profit_total * segment_shares[:, 0]
    profit_private = profit_total * segment_shares[:, 1]
    profit_corporate = profit_total * segment_shares[:, 2]

    # Risk metrics
    npl_ratio = np.clip(
        rng.normal(cfg.npl_base_pct, cfg.volatility_pct * 2.0, size=periods), 0.5, 9.0
    )
    market_var_bps = np.clip(
        rng.normal(cfg.var_base_bps, cfg.volatility_pct * 100.0, size=periods), 40.0, 350.0
    )
    lcr_pct = np.clip(
        rng.normal(cfg.lcr_base_pct, cfg.volatility_pct * 100.0, size=periods), 70.0, 200.0
    )
    cpty_exposure = np.clip(
        rng.normal(2200.0, 300.0 * (1 + cfg.volatility_pct), size=periods), 1000.0, 4000.0
    )

    df = pd.DataFrame(
        {
            "date": dates,
            "revenue_chf_m": revenue,
            "gross_margin_chf_m": gross_margin,
            "margin_pct": margin_pct * 100.0,
            "deposits_chf_m": deposits,
            "deposits_growth_pct": deposits_growth,
            "aum_chf_m": aum,
            "profit_retail_chf_m": profit_retail,
            "profit_private_chf_m": profit_private,
            "profit_corporate_chf_m": profit_corporate,
            "npl_ratio_pct": npl_ratio,
            "market_var_bps": market_var_bps,
            "lcr_pct": lcr_pct,
            "counterparty_exposure_chf_m": cpty_exposure,
        }
    ).set_index("date")

    return df


def compute_kpis(df: pd.DataFrame) -> Dict[str, float]:
    last = df.iloc[-1]
    kpis = {
        "revenue_chf_m": float(last["revenue_chf_m"]),
        "margin_pct": float(last["margin_pct"]),
        "deposits_chf_m": float(last["deposits_chf_m"]),
        "deposits_growth_pct": float(last["deposits_growth_pct"]),
        "aum_chf_m": float(last["aum_chf_m"]),
        "profit_total_chf_m": float(
            last["profit_retail_chf_m"]
            + last["profit_private_chf_m"]
            + last["profit_corporate_chf_m"]
        ),
    }
    return kpis


def compute_risk_indicators(df: pd.DataFrame) -> Dict[str, float]:
    last = df.iloc[-1]
    risks = {
        "npl_ratio_pct": float(last["npl_ratio_pct"]),
        "market_var_bps": float(last["market_var_bps"]),
        "lcr_pct": float(last["lcr_pct"]),
        "counterparty_exposure_chf_m": float(last["counterparty_exposure_chf_m"]),
    }
    return risks


def format_currency_chf_m(value: float) -> str:
    return f"CHF {value:,.1f} m".replace(",", " ")


def format_pct(value: float) -> str:
    return f"{value:,.2f}%".replace(",", " ")


