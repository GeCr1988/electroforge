"""Teste pentru dimensionarea secțiunii de cablu.

NOTĂ: valorile din backend/app/standards/curenti_admisibili.json sunt marcate
`_todo` — reconstituite din practică inginerească uzuală, nu citate direct din
I7-2011/HD 60364-5-52. Testele de mai jos verifică *logica* de dimensionare
(alegerea celei mai mici secțiuni conforme, atât la curent admisibil cât și la
cădere de tensiune) pe baza datelor curente din JSON; dacă valorile normative
sunt actualizate după verificare, aceste teste trebuie recalculate.
"""
import pytest

from app.calc_engine.sectiune_cablu import alege_sectiune_cablu


def test_alege_cea_mai_mica_sectiune_cand_lungimea_e_mica():
    # 15A, mod B1, monofazat, 230V, lungime mică -> cădere de tensiune neglijabilă,
    # deci alege 1.5mm² (17.5A admisibil >= 15A) direct.
    rezultat = alege_sectiune_cablu(
        curent_nominal_a=15,
        mod_pozare="B1",
        tip_circuit="monofazat",
        lungime_m=5,
        tensiune_v=230,
        tip_utilizare="iluminat",
    )
    assert rezultat is not None
    assert rezultat.sectiune_mm2 == 1.5
    assert rezultat.conform is True
    assert rezultat.cadere_tensiune_procent == pytest.approx(0.9783, abs=1e-3)


def test_cadere_tensiune_forteaza_sectiune_mai_mare_pe_lungime_mare():
    # Aceiași 15A, dar lungime 50m -> 1.5mm² și 2.5mm² depășesc limita de 5%
    # (forță); prima secțiune conformă e 4mm².
    rezultat = alege_sectiune_cablu(
        curent_nominal_a=15,
        mod_pozare="B1",
        tip_circuit="monofazat",
        lungime_m=50,
        tensiune_v=230,
        tip_utilizare="forta",
    )
    assert rezultat is not None
    assert rezultat.sectiune_mm2 == 4
    assert rezultat.conform is True
    assert rezultat.cadere_tensiune_procent == pytest.approx(3.668, abs=1e-2)


def test_none_cand_niciun_curent_admisibil_nu_acopera_cerinta():
    # 500A depășește curentul admisibil al celei mai mari secțiuni din tabelul B1 (120mm² -> 269A)
    rezultat = alege_sectiune_cablu(
        curent_nominal_a=500,
        mod_pozare="B1",
        tip_circuit="monofazat",
        lungime_m=5,
        tensiune_v=230,
        tip_utilizare="forta",
    )
    assert rezultat is None


def test_trifazat_foloseste_formula_cu_radical_3():
    # trifazat: ΔU% = √3 * rho * L * I / S / U * 100
    # = 1.7320508 * 0.0225 * 50 * 15 / 1.5 / 400 * 100 ≈ 4.8714%
    # sub limita de 5% (forță) încă la 1.5mm² -> nu mai e nevoie să urce la 4mm²
    # cum se întâmplă la monofazat (unde ΔU e dublă față de trifazat, la aceeași secțiune).
    rezultat = alege_sectiune_cablu(
        curent_nominal_a=15,
        mod_pozare="B1",
        tip_circuit="trifazat",
        lungime_m=50,
        tensiune_v=400,
        tip_utilizare="forta",
    )
    assert rezultat is not None
    assert rezultat.sectiune_mm2 == 1.5
    assert rezultat.conform is True
    assert rezultat.cadere_tensiune_procent == pytest.approx(4.8714, abs=1e-3)
