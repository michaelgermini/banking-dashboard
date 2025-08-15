from __future__ import annotations

import tempfile
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from data import (
    compute_kpis,
    compute_risk_indicators,
    format_currency_chf_m,
    format_pct,
    generate_financial_data,
)
from reporting import generate_pdf_from_html, render_html_report


st.set_page_config(
    page_title="Direction bancaire - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def get_data(periods: int, scenario: str) -> pd.DataFrame:
    return generate_financial_data(periods=periods, scenario=scenario)


def make_revenue_chart(df: pd.DataFrame):
    fig = px.line(
        df.reset_index(),
        x="date",
        y=["revenue_chf_m", "gross_margin_chf_m"],
        labels={"value": "CHF m", "date": "Date", "variable": "Série"},
        title="Chiffre d'affaires et marge",
    )
    fig.update_layout(legend_title_text="")
    return fig


def make_balance_chart(df: pd.DataFrame):
    fig = px.line(
        df.reset_index(),
        x="date",
        y=["deposits_chf_m", "aum_chf_m"],
        labels={"value": "CHF m", "date": "Date", "variable": "Série"},
        title="Dépôts et encours (AUM)",
    )
    fig.update_layout(legend_title_text="")
    return fig


def make_profit_chart(df: pd.DataFrame):
    fig = px.area(
        df.reset_index(),
        x="date",
        y=[
            "profit_retail_chf_m",
            "profit_private_chf_m",
            "profit_corporate_chf_m",
        ],
        labels={"value": "CHF m", "date": "Date", "variable": "Segment"},
        title="Résultat par segment",
    )
    fig.update_layout(legend_title_text="")
    return fig


def make_risk_chart(df: pd.DataFrame):
    fig = px.line(
        df.reset_index(),
        x="date",
        y=["npl_ratio_pct", "market_var_bps", "lcr_pct"],
        labels={"value": "", "date": "Date", "variable": "Indicateur"},
        title="Indicateurs de risque",
    )
    fig.update_layout(legend_title_text="")
    return fig


def save_figures_to_temp(figs: dict[str, any], temp_dir: Path) -> dict[str, str]:
    # Requires the 'kaleido' package
    paths: dict[str, str] = {}
    for name, fig in figs.items():
        out = temp_dir / f"{name}.png"
        fig.write_image(str(out), width=960, height=540, scale=2)
        paths[name] = str(out)
    return paths


def main():
    st.title("📊 Tableau de bord de direction bancaire")
    st.caption(
        "Suivi de la performance, des risques et génération de rapports (démo)."
    )

    with st.sidebar:
        st.header("Paramètres")
        scenario = st.selectbox("Scénario", ["Baseline", "Adverse", "Severe"], index=0)
        periods = st.slider("Nombre de mois", min_value=12, max_value=60, value=36)
        st.markdown("---")
        st.markdown("**Export**")
        include_charts_in_pdf = st.checkbox(
            "Inclure les graphiques dans le PDF", value=True
        )

    df = get_data(periods=periods, scenario=scenario)
    kpis = compute_kpis(df)
    risks = compute_risk_indicators(df)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "CA (dernier mois)",
        format_currency_chf_m(kpis["revenue_chf_m"]),
    )
    col2.metric("Marge", format_pct(kpis["margin_pct"]))
    col3.metric(
        "Dépôts",
        format_currency_chf_m(kpis["deposits_chf_m"]),
        f"{kpis['deposits_growth_pct']:+.2f}%",
    )
    col4.metric("AUM", format_currency_chf_m(kpis["aum_chf_m"]))

    col5, col6 = st.columns(2)
    col5.metric(
        "Résultat opérationnel",
        format_currency_chf_m(kpis["profit_total_chf_m"]),
    )
    # Risk alerts
    with col6:
        if risks["lcr_pct"] < 100:
            st.error(f"LCR sous seuil: {risks['lcr_pct']:.0f}% (< 100%)")
        elif risks["lcr_pct"] < 120:
            st.warning(f"LCR à surveiller: {risks['lcr_pct']:.0f}%")
        else:
            st.success(f"LCR confortable: {risks['lcr_pct']:.0f}%")

        if risks["npl_ratio_pct"] > 3.0:
            st.warning(f"NPL ratio élevé: {risks['npl_ratio_pct']:.2f}% (> 3%)")
        if risks["market_var_bps"] > 150:
            st.warning(f"VaR élevée: {risks['market_var_bps']:.0f} bps")

    st.markdown("---")

    # Charts
    fig_revenue = make_revenue_chart(df)
    fig_balance = make_balance_chart(df)
    fig_profit = make_profit_chart(df)
    fig_risk = make_risk_chart(df)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_revenue, use_container_width=True)
        st.plotly_chart(fig_profit, use_container_width=True)
    with c2:
        st.plotly_chart(fig_balance, use_container_width=True)
        st.plotly_chart(fig_risk, use_container_width=True)

    # Report export
    st.subheader("Export du rapport PDF")
    st.caption(
        "Génère un rapport PDF avec KPIs, risques et graphiques (xhtml2pdf)."
    )

    if st.button("Générer le PDF"):
        with st.spinner("Génération du rapport..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp = Path(tmpdir)
                figures = {}
                if include_charts_in_pdf:
                    fig_paths = save_figures_to_temp(
                        {
                            "revenue_chart": fig_revenue,
                            "balance_chart": fig_balance,
                            "profit_chart": fig_profit,
                            "risk_chart": fig_risk,
                        },
                        tmp,
                    )
                    figures = fig_paths

                period_start = df.index.min().strftime("%b %Y")
                period_end = df.index.max().strftime("%b %Y")

                context = {
                    "scenario": scenario,
                    "period_start": period_start,
                    "period_end": period_end,
                    "kpis": {
                        "revenue_fmt": format_currency_chf_m(kpis["revenue_chf_m"]),
                        "margin_fmt": format_pct(kpis["margin_pct"]),
                        "deposits_fmt": format_currency_chf_m(kpis["deposits_chf_m"]),
                        "deposits_growth_fmt": f"{kpis['deposits_growth_pct']:.2f}%",
                        "aum_fmt": format_currency_chf_m(kpis["aum_chf_m"]),
                        "profit_fmt": format_currency_chf_m(
                            kpis["profit_total_chf_m"]
                        ),
                    },
                    "risks": {
                        "npl_fmt": f"{risks['npl_ratio_pct']:.2f}%",
                        "var_fmt": f"{risks['market_var_bps']:.0f} bps",
                        "lcr_fmt": f"{risks['lcr_pct']:.0f}%",
                        "cpty_fmt": format_currency_chf_m(
                            risks["counterparty_exposure_chf_m"]
                        ),
                    },
                    "figures": figures,
                }

                html = render_html_report(context)
                pdf_bytes = generate_pdf_from_html(html)
                st.download_button(
                    label="Télécharger le rapport PDF",
                    data=pdf_bytes,
                    file_name="rapport_direction.pdf",
                    mime="application/pdf",
                )


if __name__ == "__main__":
    main()


