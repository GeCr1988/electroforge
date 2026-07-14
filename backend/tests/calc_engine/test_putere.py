from app.calc_engine.putere import calc_putere_calcul, calc_putere_instalata


def test_putere_instalata_suma_simpla():
    assert calc_putere_instalata([100, 200, 300]) == 600


def test_putere_instalata_lista_goala():
    assert calc_putere_instalata([]) == 0


def test_putere_calcul_aplica_ku_apoi_ks():
    # (1000*1.0 + 2000*0.2) * 0.8 = (1000 + 400) * 0.8 = 1120
    receptori = [(1000, 1.0), (2000, 0.2)]
    assert calc_putere_calcul(receptori, ks=0.8) == 1120


def test_putere_calcul_ks_1_egal_cu_suma_utilizata():
    receptori = [(500, 0.5), (500, 0.5)]
    assert calc_putere_calcul(receptori, ks=1.0) == 500
