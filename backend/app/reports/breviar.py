"""Generare breviar de calcul (memoriu + rezultate + BOM + schemă) — HTML
randat cu Jinja2, convertit în PDF cu WeasyPrint.

Importul WeasyPrint e amânat (lazy) în `genereaza_pdf_breviar`, ca restul
aplicației (și `genereaza_html_breviar`, testabil independent) să nu depindă
de bibliotecile native Pango/GTK necesare de WeasyPrint doar la randarea PDF.
"""
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
)


def genereaza_html_breviar(
    proiect: dict,
    tablouri: list[dict],
    schema_svg: str,
    bom_linii: list[dict],
    bom_cost_total: float,
) -> str:
    """Randează template-ul HTML al breviarului. Parametrii sunt dict-uri
    simple (nu modele SQLAlchemy), ca funcția să rămână testabilă izolat.
    """
    template = _env.get_template("breviar.html")
    return template.render(
        proiect=proiect,
        tablouri=tablouri,
        schema_svg=schema_svg,
        bom_linii=bom_linii,
        bom_cost_total=bom_cost_total,
    )


def genereaza_pdf_breviar(html: str) -> bytes:
    from weasyprint import HTML

    return HTML(string=html).write_pdf()
