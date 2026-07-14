"""Calcul curent de scurtcircuit (Isc) minim la capătul circuitului.

Referință: I7-2011 (verificare declanșare automată în timpul admis la
atingere indirectă). Bucla de defect folosită e monofazată (fază-nul/PE),
cu tensiunea de fază U0 (~230V), indiferent dacă circuitul e monofazat sau
trifazat — defectul relevant pentru acest calcul e mereu un defect simplu
fază-nul.

Reactanța cablului e neglijată (se consideră doar rezistența) — practică
uzuală pentru secțiuni mici. `_todo`: verifică cu I7-2011/HD 60364 dacă
reactanța trebuie inclusă pentru secțiuni mari (>=95mm²), unde nu mai e
neglijabilă.

Isc la ORIGINEA instalației (lângă sursă, folosit pt verificarea puterii de
rupere Icu a protecțiilor) necesită impedanța rețelei amonte de la
distribuitor — dată care nu poate fi presupusă (variază enorm de la un punct
de racordare la altul). Acest modul nu inventează o valoare implicită: dacă
impedanța amonte nu e cunoscută, apelantul (vezi app/api/calcule.py) trebuie
să trateze explicit acest caz ca "date insuficiente", nu să substituie 0.
"""

U0_FAZA_NUL_V = 230.0


def calc_impedanta_cablu(lungime_m: float, sectiune_mm2: float, rho_ohm_mm2_per_m: float) -> float:
    """Rezistența cablului pe un sens (dus sau întors), în ohm."""
    return rho_ohm_mm2_per_m * lungime_m / sectiune_mm2


def calc_isc_minim_capat_circuit(
    impedanta_amonte_ohm: float,
    lungime_m: float,
    sectiune_mm2: float,
    rho_ohm_mm2_per_m: float,
    u0_v: float = U0_FAZA_NUL_V,
) -> float:
    """Isc minim (A) la capătul circuitului, pentru verificarea declanșării automate.

    Zbuclă = impedanța amonte + rezistența cablului dus-întors (2×R).
    """
    r_cablu = calc_impedanta_cablu(lungime_m, sectiune_mm2, rho_ohm_mm2_per_m)
    z_bucla = impedanta_amonte_ohm + 2 * r_cablu
    return u0_v / z_bucla
