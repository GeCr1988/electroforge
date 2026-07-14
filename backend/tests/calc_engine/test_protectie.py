from app.calc_engine.protectie import alege_cablu, alege_protectie

PROTECTII = [
    {"id": 1, "in_a": 16, "icu_ka": 6},
    {"id": 2, "in_a": 20, "icu_ka": 6},
    {"id": 3, "in_a": 32, "icu_ka": 10},
]

CABLURI = [
    {"id": 10, "sectiune_mm2": 1.5},
    {"id": 11, "sectiune_mm2": 2.5},
    {"id": 12, "sectiune_mm2": 6},
]


def test_alege_protectie_cea_mai_mica_valida():
    rezultat = alege_protectie(PROTECTII, curent_nominal_a=15, isc_a=500)
    assert rezultat["id"] == 1


def test_alege_protectie_sare_peste_cea_cu_in_insuficient():
    rezultat = alege_protectie(PROTECTII, curent_nominal_a=18, isc_a=500)
    assert rezultat["id"] == 2


def test_alege_protectie_filtreaza_dupa_icu():
    # Isc foarte mare -> doar protecția cu Icu=10kA (id 3) satisface
    rezultat = alege_protectie(PROTECTII, curent_nominal_a=15, isc_a=9000)
    assert rezultat["id"] == 3


def test_alege_protectie_none_daca_nimic_nu_satisface():
    rezultat = alege_protectie(PROTECTII, curent_nominal_a=100, isc_a=500)
    assert rezultat is None


def test_alege_cablu_cea_mai_mica_valida():
    rezultat = alege_cablu(CABLURI, sectiune_necesara_mm2=1.5)
    assert rezultat["id"] == 10


def test_alege_cablu_urca_la_urmatoarea_sectiune():
    rezultat = alege_cablu(CABLURI, sectiune_necesara_mm2=4)
    assert rezultat["id"] == 12


def test_alege_cablu_none_daca_nimic_nu_satisface():
    rezultat = alege_cablu(CABLURI, sectiune_necesara_mm2=50)
    assert rezultat is None
