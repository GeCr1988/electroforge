import pytest

from app.calc_engine.scurtcircuit import calc_impedanta_cablu, calc_isc_minim_capat_circuit


def test_impedanta_cablu():
    # R = rho * L / S = 0.0225 * 20 / 2.5 = 0.18 ohm
    assert calc_impedanta_cablu(lungime_m=20, sectiune_mm2=2.5, rho_ohm_mm2_per_m=0.0225) == pytest.approx(0.18)


def test_isc_minim_capat_circuit():
    # Zbuclă = 0.1 (amonte) + 2*0.18 (cablu) = 0.46 ohm
    # Isc = 230 / 0.46 = 500A
    isc = calc_isc_minim_capat_circuit(
        impedanta_amonte_ohm=0.1, lungime_m=20, sectiune_mm2=2.5, rho_ohm_mm2_per_m=0.0225
    )
    assert isc == pytest.approx(500.0)


def test_isc_scade_cu_lungimea_mai_mare():
    isc_scurt = calc_isc_minim_capat_circuit(
        impedanta_amonte_ohm=0.1, lungime_m=10, sectiune_mm2=2.5, rho_ohm_mm2_per_m=0.0225
    )
    isc_lung = calc_isc_minim_capat_circuit(
        impedanta_amonte_ohm=0.1, lungime_m=50, sectiune_mm2=2.5, rho_ohm_mm2_per_m=0.0225
    )
    assert isc_lung < isc_scurt


def test_isc_creste_cu_sectiune_mai_mare():
    isc_mica = calc_isc_minim_capat_circuit(
        impedanta_amonte_ohm=0.1, lungime_m=20, sectiune_mm2=1.5, rho_ohm_mm2_per_m=0.0225
    )
    isc_mare = calc_isc_minim_capat_circuit(
        impedanta_amonte_ohm=0.1, lungime_m=20, sectiune_mm2=6, rho_ohm_mm2_per_m=0.0225
    )
    assert isc_mare > isc_mica
