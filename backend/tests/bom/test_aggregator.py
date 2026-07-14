from app.bom.aggregator import agrega_bom


def test_sumeaza_cantitatile_aceleiasi_componente():
    intrari = [
        {"componenta_id": 1, "nume": "Cablu 1.5", "categorie": "cablu", "unitate_masura": "m", "cantitate": 15, "pret_estimativ": 2.5},
        {"componenta_id": 1, "nume": "Cablu 1.5", "categorie": "cablu", "unitate_masura": "m", "cantitate": 10, "pret_estimativ": 2.5},
    ]
    linii, total = agrega_bom(intrari)
    assert len(linii) == 1
    assert linii[0]["cantitate_totala"] == 25
    assert linii[0]["cost_total"] == 62.5
    assert total == 62.5


def test_componente_diferite_raman_separate():
    intrari = [
        {"componenta_id": 1, "nume": "A", "categorie": "cablu", "unitate_masura": "m", "cantitate": 10, "pret_estimativ": 1.0},
        {"componenta_id": 2, "nume": "B", "categorie": "protectie", "unitate_masura": "buc", "cantitate": 1, "pret_estimativ": 25.0},
    ]
    linii, total = agrega_bom(intrari)
    assert len(linii) == 2
    assert total == 35.0


def test_fara_pret_estimativ_cost_none_si_nu_afecteaza_totalul():
    intrari = [
        {"componenta_id": 1, "nume": "A", "categorie": "cablu", "unitate_masura": "m", "cantitate": 10, "pret_estimativ": None},
        {"componenta_id": 2, "nume": "B", "categorie": "protectie", "unitate_masura": "buc", "cantitate": 1, "pret_estimativ": 25.0},
    ]
    linii, total = agrega_bom(intrari)
    linie_fara_pret = next(l for l in linii if l["componenta_id"] == 1)
    assert linie_fara_pret["cost_total"] is None
    assert total == 25.0


def test_lista_goala():
    linii, total = agrega_bom([])
    assert linii == []
    assert total == 0.0
