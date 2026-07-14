from app.reports.breviar import genereaza_html_breviar

PROIECT = {
    "nume": "Casa Ion",
    "beneficiar": "Ion Popescu",
    "tip_cladire": "rezidential",
    "tensiune_alimentare": "230/400V",
    "adresa": "Str. Exemplu 1",
}

TABLOURI = [
    {
        "nume": "TE",
        "putere_instalata": 200.0,
        "putere_calcul": 200.0,
        "circuite": [
            {
                "nume": "C1 iluminat",
                "tip": "monofazat",
                "mod_pozare": "B1",
                "lungime_cablu_m": 15,
                "receptori": [
                    {"nume": "Bec 1", "tip": "iluminat", "putere_nominala_w": 100, "cos_phi": 1.0, "ku": 1.0, "ks": 1.0},
                ],
                "rezultate": [
                    {
                        "tip_calcul": "curent_nominal",
                        "valoare": 0.87,
                        "unitate": "A",
                        "standard_referinta": "I7-2011",
                        "status_conformitate": "conform",
                    },
                ],
            }
        ],
    }
]


def test_html_contine_datele_proiectului():
    html = genereaza_html_breviar(PROIECT, TABLOURI, schema_svg="<svg></svg>", bom_linii=[], bom_cost_total=0.0)
    assert "Casa Ion" in html
    assert "Ion Popescu" in html
    assert "Str. Exemplu 1" in html


def test_html_contine_disclaimer_legal():
    html = genereaza_html_breviar(PROIECT, TABLOURI, schema_svg="<svg></svg>", bom_linii=[], bom_cost_total=0.0)
    assert "inginer atestat" in html.lower()


def test_html_contine_circuite_si_rezultate():
    html = genereaza_html_breviar(PROIECT, TABLOURI, schema_svg="<svg></svg>", bom_linii=[], bom_cost_total=0.0)
    assert "C1 iluminat" in html
    assert "curent_nominal" in html
    assert "conform" in html


def test_html_contine_schema_svg_embedata():
    html = genereaza_html_breviar(
        PROIECT, TABLOURI, schema_svg='<svg><text>MARKER_UNIC</text></svg>', bom_linii=[], bom_cost_total=0.0
    )
    assert "MARKER_UNIC" in html


def test_html_contine_bom():
    bom_linii = [
        {"nume": "Cablu FY 1.5", "categorie": "cablu", "cantitate_totala": 15, "unitate_masura": "m", "pret_estimativ": 2.5, "cost_total": 37.5}
    ]
    html = genereaza_html_breviar(PROIECT, TABLOURI, schema_svg="<svg></svg>", bom_linii=bom_linii, bom_cost_total=37.5)
    assert "Cablu FY 1.5" in html
    assert "37.50" in html
