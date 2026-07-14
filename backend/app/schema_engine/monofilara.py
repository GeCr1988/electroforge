"""Generator de schemă monofilară SVG — layout simplu pe niveluri fixe
(sursă → tablou(uri) → circuite), nu un layout de graf general.

Nu sunt simboluri IEC 60617 pixel-perfect — o bibliotecă mică de simboluri
recognoscibile (sursă/disjunctor/receptor), suficientă pentru MVP. Câmpul
`simbol_ref` din `ComponentaCatalog` e pregătit pentru o bibliotecă mai
bogată mai târziu, fără să schimbe structura generatorului.

Funcțiile primesc structuri de date simple (dict), nu modele SQLAlchemy, ca
modulul să rămână testabil izolat de DB.
"""

LEAF_WIDTH = 160
BOX_W, BOX_H = 140, 50
CIRCUIT_BOX_H = 70


def _defs_simboluri() -> str:
    return """
  <defs>
    <symbol id="sym-sursa" viewBox="0 0 16 16">
      <circle cx="8" cy="8" r="7" fill="none" stroke="currentColor" stroke-width="1.5" />
      <path d="M4 8 L12 8 M8 4 L8 12" stroke="currentColor" stroke-width="1.5" />
    </symbol>
    <symbol id="sym-disjunctor" viewBox="0 0 16 16">
      <rect x="2" y="2" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" />
      <path d="M4 12 L12 4" stroke="currentColor" stroke-width="1.5" />
    </symbol>
    <symbol id="sym-receptor" viewBox="0 0 16 16">
      <circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5" />
      <path d="M4 4 L12 12 M4 12 L12 4" stroke="currentColor" stroke-width="1" />
    </symbol>
  </defs>
""".strip("\n")


def _linie(x1: float, y1: float, x2: float, y2: float) -> str:
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="currentColor" stroke-width="1.5" />'


def _cutie(x: float, y: float, w: float, h: float, linii: list[str], simbol: str) -> str:
    text_x = x + w / 2
    tspans = "".join(
        f'<tspan x="{text_x:.1f}" dy="{"0" if i == 0 else "14"}">{_escape(t)}</tspan>' for i, t in enumerate(linii)
    )
    text_y = y + 20 if len(linii) > 1 else y + h / 2 + 4
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'fill="none" stroke="currentColor" stroke-width="1.5" rx="4" />'
        f'<use href="#sym-{simbol}" x="{x + 6:.1f}" y="{y + 6:.1f}" width="14" height="14" />'
        f'<text x="{text_x:.1f}" y="{text_y:.1f}" text-anchor="middle">{tspans}</text>'
    )


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def genereaza_schema_monofilara(nume_proiect: str, tensiune_alimentare: str, tablouri: list[dict]) -> str:
    """tablouri: listă de dict {"nume": str, "circuite": [{"nume": str,
    "sectiune_mm2": float | None, "protectie_nume": str | None}]}
    """
    total_leaves = sum(max(len(t["circuite"]), 1) for t in tablouri) or 1
    canvas_w = max(420, total_leaves * LEAF_WIDTH)
    canvas_h = 260 + CIRCUIT_BOX_H

    sursa_x = canvas_w / 2
    sursa_y = 20
    tablou_y = 110
    circuit_y = 200

    parti = [
        f'<svg viewBox="0 0 {canvas_w} {canvas_h}" xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" font-family="sans-serif" font-size="11" color="#1f2937">',
        f"<!-- schema monofilara: {_escape(nume_proiect)} -->",
        _defs_simboluri(),
        _linie(sursa_x, sursa_y + BOX_H, sursa_x, tablou_y) if tablouri else "",
        _cutie(sursa_x - BOX_W / 2, sursa_y, BOX_W, BOX_H, [f"Alimentare {tensiune_alimentare}"], "sursa"),
    ]

    cursor_x = 0.0
    for tablou in tablouri:
        circuite = tablou["circuite"]
        n = max(len(circuite), 1)
        span_w = n * LEAF_WIDTH
        tablou_cx = cursor_x + span_w / 2

        parti.append(_linie(sursa_x, sursa_y + BOX_H, tablou_cx, tablou_y))
        parti.append(_cutie(tablou_cx - BOX_W / 2, tablou_y, BOX_W, BOX_H, [tablou["nume"]], "sursa"))

        for i, c in enumerate(circuite):
            cx = cursor_x + i * LEAF_WIDTH + LEAF_WIDTH / 2
            box_w = LEAF_WIDTH - 20
            detalii = []
            if c.get("sectiune_mm2") is not None:
                detalii.append(f'{c["sectiune_mm2"]}mm²')
            if c.get("protectie_nume"):
                detalii.append(c["protectie_nume"])
            linii = [c["nume"]] + ([" · ".join(detalii)] if detalii else [])

            parti.append(_linie(tablou_cx, tablou_y + BOX_H, cx, circuit_y))
            parti.append(_cutie(cx - box_w / 2, circuit_y, box_w, CIRCUIT_BOX_H, linii, "disjunctor"))

        cursor_x += span_w

    parti.append("</svg>")
    return "\n".join(p for p in parti if p)
