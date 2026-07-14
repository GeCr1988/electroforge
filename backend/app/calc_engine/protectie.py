"""Alegere automată a componentelor din catalog (selectivitate protecții,
sugestie cablu) — funcții pure, independente de DB.

Candidații sunt liste de dict simple (nu modele SQLAlchemy), extrase din
`ComponentaCatalog.specificatii`, ca acest modul să rămână testabil izolat.
"""


def alege_protectie(candidati: list[dict], curent_nominal_a: float, isc_a: float) -> dict | None:
    """Alege cea mai mică protecție (după In) care satisface simultan:
    - In >= curent_nominal_a (protecția nu declanșează la sarcină normală)
    - Icu (kA -> A) >= isc_a (putere de rupere suficientă la scurtcircuit)

    `candidati`: listă de dict cu cheile "id", "in_a", "icu_ka".
    Întoarce None dacă niciun candidat nu satisface ambele condiții.
    """
    valizi = [c for c in candidati if c["in_a"] >= curent_nominal_a and c["icu_ka"] * 1000 >= isc_a]
    if not valizi:
        return None
    return min(valizi, key=lambda c: c["in_a"])


def alege_cablu(candidati: list[dict], sectiune_necesara_mm2: float) -> dict | None:
    """Alege cel mai mic cablu din catalog cu secțiune >= cea calculată de motor.

    `candidati`: listă de dict cu cheile "id", "sectiune_mm2".
    """
    valizi = [c for c in candidati if c["sectiune_mm2"] >= sectiune_necesara_mm2]
    if not valizi:
        return None
    return min(valizi, key=lambda c: c["sectiune_mm2"])
