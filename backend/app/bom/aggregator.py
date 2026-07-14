"""Agregare BOM: sumează cantitățile componentelor selectate (cabluri +
protecții pe circuite, componente pe receptori) dintr-un proiect, grupate pe
componentă. Funcție pură — primește intrări ca dict-uri simple, nu modele
SQLAlchemy, ca să rămână testabilă izolat de DB.
"""


def agrega_bom(intrari: list[dict]) -> tuple[list[dict], float]:
    """`intrari`: listă de dict cu cheile "componenta_id", "nume", "categorie",
    "unitate_masura", "cantitate", "pret_estimativ" (poate fi None).

    Întoarce (linii_agregate, cost_total_general). O linie fără preț estimativ
    are cost_total=None și nu contribuie la totalul general (nu presupunem 0).
    """
    grupuri: dict[int, dict] = {}
    for intrare in intrari:
        cid = intrare["componenta_id"]
        grup = grupuri.setdefault(
            cid,
            {
                "componenta_id": cid,
                "nume": intrare["nume"],
                "categorie": intrare["categorie"],
                "unitate_masura": intrare["unitate_masura"],
                "cantitate_totala": 0.0,
                "pret_estimativ": intrare["pret_estimativ"],
            },
        )
        grup["cantitate_totala"] += intrare["cantitate"]

    linii = []
    cost_total_general = 0.0
    for grup in grupuri.values():
        pret = grup["pret_estimativ"]
        cost = grup["cantitate_totala"] * pret if pret is not None else None
        linii.append({**grup, "cost_total": cost})
        if cost is not None:
            cost_total_general += cost

    return linii, cost_total_general
