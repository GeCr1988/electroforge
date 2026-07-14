import pytest


def test_flux_complet_proiect_pana_la_calcul(client, auth_headers):
    headers = auth_headers()

    resp = client.post(
        "/proiecte",
        headers=headers,
        json={
            "nume": "Casa Ion",
            "beneficiar": "Ion Popescu",
            "tip_cladire": "rezidential",
            "adresa": "Str. Exemplu 1",
            "tensiune_alimentare": "230/400V",
        },
    )
    assert resp.status_code == 201
    proiect_id = resp.json()["id"]

    resp = client.post(f"/proiecte/{proiect_id}/tablouri", headers=headers, json={"nume": "TE"})
    assert resp.status_code == 201
    tablou_id = resp.json()["id"]

    resp = client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C1 iluminat living", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 15},
    )
    assert resp.status_code == 201
    circuit_id = resp.json()["id"]

    for nume in ("Corp iluminat 1", "Corp iluminat 2"):
        resp = client.post(
            f"/circuite/{circuit_id}/receptori",
            headers=headers,
            json={"nume": nume, "tip": "iluminat", "putere_nominala_w": 100, "cos_phi": 1.0, "ku": 1.0, "ks": 1.0},
        )
        assert resp.status_code == 201

    resp = client.post(f"/circuite/{circuit_id}/calculeaza", headers=headers)
    assert resp.status_code == 200
    rezultate = {r["tip_calcul"]: r for r in resp.json()}

    assert rezultate["curent_nominal"]["valoare"] == pytest.approx(0.8696, abs=1e-3)
    assert rezultate["curent_nominal"]["status_conformitate"] == "conform"

    assert rezultate["sectiune_cablu"]["valoare"] == pytest.approx(1.5)
    assert rezultate["sectiune_cablu"]["status_conformitate"] == "conform"

    assert rezultate["cadere_tensiune"]["valoare"] == pytest.approx(0.1701, abs=1e-3)
    assert rezultate["cadere_tensiune"]["status_conformitate"] == "conform"

    resp = client.get(f"/tablouri/{tablou_id}", headers=headers)
    tablou = resp.json()
    assert tablou["putere_instalata"] == pytest.approx(200.0)
    assert tablou["putere_calcul"] == pytest.approx(200.0)
