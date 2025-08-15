from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa


def render_html_report(context: Dict[str, Any]) -> str:
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("report.html")
    html = template.render(**context)
    return html


def generate_pdf_from_html(html: str) -> bytes:
    buffer = BytesIO()
    # xhtml2pdf expects UTF-8
    result = pisa.CreatePDF(src=html, dest=buffer, encoding="UTF-8")
    if result.err:
        # Return whatever was generated to aid debugging
        return buffer.getvalue()
    return buffer.getvalue()


