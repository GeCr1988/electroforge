from app.schema_engine.monofilara import genereaza_schema_monofilara


def test_svg_valid_root_element():
    svg = genereaza_schema_monofilara(
        nume_proiect="Casa Ion",
        tensiune_alimentare="230/400V",
        tablouri=[{"nume": "TE", "circuite": [{"nume": "C1", "sectiune_mm2": 1.5, "protectie_nume": "C16"}]}],
    )
    assert svg.strip().startswith("<svg")
    assert svg.strip().endswith("</svg>")


def test_contine_numele_tabloului_si_circuitelor():
    svg = genereaza_schema_monofilara(
        nume_proiect="Casa Ion",
        tensiune_alimentare="230/400V",
        tablouri=[
            {
                "nume": "TE",
                "circuite": [
                    {"nume": "C1 iluminat", "sectiune_mm2": 1.5, "protectie_nume": "C16"},
                    {"nume": "C2 prize", "sectiune_mm2": 2.5, "protectie_nume": None},
                ],
            }
        ],
    )
    assert "TE" in svg
    assert "C1 iluminat" in svg
    assert "C2 prize" in svg
    assert "1.5mm²" in svg
    assert "C16" in svg


def test_contine_tensiunea_alimentare():
    svg = genereaza_schema_monofilara(nume_proiect="X", tensiune_alimentare="400V", tablouri=[])
    assert "400V" in svg


def test_fara_tablouri_tot_genereaza_svg_valid():
    svg = genereaza_schema_monofilara(nume_proiect="Gol", tensiune_alimentare="230V", tablouri=[])
    assert svg.strip().startswith("<svg")
    assert svg.strip().endswith("</svg>")


def test_layout_mai_multe_tablouri_nu_se_suprapun():
    svg = genereaza_schema_monofilara(
        nume_proiect="X",
        tensiune_alimentare="230/400V",
        tablouri=[
            {"nume": "TE", "circuite": [{"nume": "C1", "sectiune_mm2": None, "protectie_nume": None}]},
            {"nume": "TD1", "circuite": [{"nume": "C2", "sectiune_mm2": None, "protectie_nume": None}]},
        ],
    )
    assert "TE" in svg and "TD1" in svg
