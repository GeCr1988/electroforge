import math

import pytest

from app.calc_engine.curent import calc_curent_monofazat, calc_curent_trifazat


def test_curent_monofazat_cos_phi_1():
    # In = P / (U * cosφ) = 2300 / (230 * 1) = 10A
    assert calc_curent_monofazat(2300, tensiune_v=230, cos_phi=1.0) == pytest.approx(10.0)


def test_curent_monofazat_cu_cos_phi():
    # In = 1000 / (230 * 0.8)
    assert calc_curent_monofazat(1000, tensiune_v=230, cos_phi=0.8) == pytest.approx(1000 / (230 * 0.8))


def test_curent_trifazat_cos_phi_1():
    # P ales astfel încât In = 10A: P = √3 * 400 * 10
    putere = math.sqrt(3) * 400 * 10
    assert calc_curent_trifazat(putere, tensiune_v=400, cos_phi=1.0) == pytest.approx(10.0)


def test_curent_trifazat_cu_cos_phi():
    putere = 10000
    asteptat = putere / (math.sqrt(3) * 400 * 0.9)
    assert calc_curent_trifazat(putere, tensiune_v=400, cos_phi=0.9) == pytest.approx(asteptat)
