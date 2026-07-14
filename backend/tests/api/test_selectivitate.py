import pytest


def _seteaza_proiect_complet(client, headers, impedanta_amonte=None):
    resp = client.post(
        "/proiecte",
        headers=headers,
        json={
            "nume": "Casa Ion",
            "beneficiar": "Ion",
            "tip_cladire": "rezidential",
            "tensiune_alimentare": "230/400V",
            "impedanta_retea_amonte_ohm": impedanta_amonte,
        },
    )
    proiect_id = resp.json()["id"]
    tablou_id = client.post(f"/proiecte/{proiect_id}/tablouri", headers=headers, json={"nume": "TE"}).json()["id"]
    circuit_id = client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C1", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 15},
    ).json()["id"]
    client.post(
        f"/circuite/{circuit_id}/receptori",
        headers=headers,
        json={"nume": "Bec", "tip": "iluminat", "putere_nominala_w": 200, "cos_phi": 1.0, "ku": 1.0, "ks": 1.0},
    )
    return proiect_id, tablou_id, circuit_id


def test_fara_impedanta_amonte_isc_e_date_insuficiente(client, auth_headers):
    headers = auth_headers()
    _, _, circuit_id = _seteaza_proiect_complet(client, headers, impedanta_amonte=None)

    resp = client.post(f"/circuite/{circuit_id}/calculeaza", headers=headers)
    rezultate = {r["tip_calcul"]: r for r in resp.json()}

    assert rezultate["isc_minim_capat_circuit"]["status_conformitate"] == "neconform"
    assert "insuficiente" in rezultate["isc_minim_capat_circuit"]["standard_referinta"]
    assert rezultate["protectie_sugerata"]["status_conformitate"] == "neconform"


def test_cu_impedanta_amonte_si_catalog_alege_automat_protectie_si_cablu(client, auth_headers):
    headers = auth_headers()
    _, _, circuit_id = _seteaza_proiect_complet(client, headers, impedanta_amonte=0.1)

    client.post("/catalog", headers=headers, json={"categorie": "protectie", "nume": "C16", "specificatii": {"in_a": 16, "icu_ka": 6}})
    client.post("/catalog", headers=headers, json={"categorie": "protectie", "nume": "C10", "specificatii": {"in_a": 10, "icu_ka": 6}})
    client.post("/catalog", headers=headers, json={"categorie": "cablu", "nume": "FY 1.5", "specificatii": {"sectiune_mm2": 1.5}})

    resp = client.post(f"/circuite/{circuit_id}/calculeaza", headers=headers)
    assert resp.status_code == 200
    rezultate = {r["tip_calcul"]: r for r in resp.json()}

    assert rezultate["isc_minim_capat_circuit"]["status_conformitate"] == "conform"
    assert rezultate["isc_minim_capat_circuit"]["valoare"] > 0

    assert rezultate["protectie_sugerata"]["status_conformitate"] == "conform"
    # putere 200W la 230V => curent nominal ~0.87A -> cea mai mică protecție (10A) satisface
    assert rezultate["protectie_sugerata"]["valoare"] == 10

    circuit = client.get(f"/circuite/{circuit_id}", headers=headers).json()
    assert circuit["protectie_selectata_id"] is not None
    assert circuit["cablu_selectat_id"] is not None
    assert circuit["protectie_auto"] is True
    assert circuit["cablu_auto"] is True


def test_suprascriere_manuala_protectie_nu_e_atinsa_la_recalcul(client, auth_headers):
    headers = auth_headers()
    _, _, circuit_id = _seteaza_proiect_complet(client, headers, impedanta_amonte=0.1)

    componenta_id = client.post(
        "/catalog", headers=headers, json={"categorie": "protectie", "nume": "C32", "specificatii": {"in_a": 32, "icu_ka": 6}}
    ).json()["id"]

    client.patch(f"/circuite/{circuit_id}", headers=headers, json={"protectie_selectata_id": componenta_id})

    resp = client.post(f"/circuite/{circuit_id}/calculeaza", headers=headers)
    assert resp.status_code == 200

    circuit = client.get(f"/circuite/{circuit_id}", headers=headers).json()
    assert circuit["protectie_selectata_id"] == componenta_id
    assert circuit["protectie_auto"] is False
