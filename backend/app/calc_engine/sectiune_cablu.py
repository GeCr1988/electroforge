"""Dimensionare secțiune cablu: curent admisibil + verificare cădere de tensiune.

Referință: specificatii-complete.md secțiunea 4.3 (curent admisibil conform mod de
pozare — HD 60364-5-52; cădere de tensiune admisă 3% iluminat / 5% forță — I7-2011).
"""
import math
from dataclasses import dataclass

from app.calc_engine.standards_loader import cadere_tensiune, curenti_admisibili, sectiuni_standard


@dataclass
class RezultatSectiune:
    sectiune_mm2: float
    curent_admisibil_a: float
    cadere_tensiune_procent: float
    limita_cadere_tensiune_procent: float
    conform_curent: bool
    conform_cadere_tensiune: bool

    @property
    def conform(self) -> bool:
        return self.conform_curent and self.conform_cadere_tensiune


def _cheie_sectiune(sectiune_mm2: float) -> str:
    return str(int(sectiune_mm2)) if sectiune_mm2 == int(sectiune_mm2) else str(sectiune_mm2)


def _cadere_tensiune_procent(
    curent_nominal_a: float, sectiune_mm2: float, lungime_m: float, tensiune_v: float, tip_circuit: str, rho: float
) -> float:
    if tip_circuit == "monofazat":
        delta_u = 2 * rho * lungime_m * curent_nominal_a / sectiune_mm2
    else:
        delta_u = math.sqrt(3) * rho * lungime_m * curent_nominal_a / sectiune_mm2
    return delta_u / tensiune_v * 100


def alege_sectiune_cablu(
    curent_nominal_a: float,
    mod_pozare: str,
    tip_circuit: str,
    lungime_m: float,
    tensiune_v: float,
    tip_utilizare: str = "forta",
) -> RezultatSectiune | None:
    """Alege cea mai mică secțiune standard care satisface curentul admisibil și
    cădere de tensiune. Întoarce None dacă nicio secțiune din tabelul normativ nu
    satisface curentul admisibil necesar.
    """
    tabel_curenti = curenti_admisibili()["moduri_pozare"][mod_pozare]["curenti_admisibili_a"]
    limite = cadere_tensiune()["limite_procentuale"]
    limita = limite.get(tip_utilizare, limite["forta"])
    rho = cadere_tensiune()["rezistivitate_cupru_ohm_mm2_per_m"]

    ultima_incercare: RezultatSectiune | None = None

    for sectiune in sorted(sectiuni_standard()):
        cheie = _cheie_sectiune(sectiune)
        if cheie not in tabel_curenti:
            continue

        curent_admisibil = tabel_curenti[cheie]
        conform_curent = curent_admisibil >= curent_nominal_a
        if not conform_curent:
            continue

        procent = _cadere_tensiune_procent(curent_nominal_a, sectiune, lungime_m, tensiune_v, tip_circuit, rho)
        conform_cadere = procent <= limita

        rezultat = RezultatSectiune(
            sectiune_mm2=sectiune,
            curent_admisibil_a=curent_admisibil,
            cadere_tensiune_procent=procent,
            limita_cadere_tensiune_procent=limita,
            conform_curent=conform_curent,
            conform_cadere_tensiune=conform_cadere,
        )
        ultima_incercare = rezultat

        if rezultat.conform:
            return rezultat

    return ultima_incercare
