def _creeaza_proiect(client, headers):
    resp = client.post(
        "/proiecte",
        headers=headers,
        json={
            "nume": "Casa Ion",
            "beneficiar": "Ion Popescu",
            "tip_cladire": "rezidential",
            "tensiune_alimentare": "230/400V",
        },
    )
    return resp.json()["id"]


def _creeaza_tablou(client, headers, proiect_id):
    resp = client.post(f"/proiecte/{proiect_id}/tablouri", headers=headers, json={"nume": "TE"})
    return resp.json()["id"]


def _creeaza_circuit(client, headers, tablou_id):
    resp = client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C1", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 10},
    )
    return resp.json()["id"]


def _creeaza_receptor(client, headers, circuit_id):
    resp = client.post(
        f"/circuite/{circuit_id}/receptori",
        headers=headers,
        json={"nume": "Bec 1", "tip": "iluminat", "putere_nominala_w": 60, "cos_phi": 1.0, "ku": 1.0, "ks": 1.0},
    )
    return resp.json()["id"]


def test_patch_proiect_partial_update(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)

    resp = client.patch(f"/proiecte/{proiect_id}", headers=headers, json={"nume": "Casa Modificată"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["nume"] == "Casa Modificată"
    assert body["beneficiar"] == "Ion Popescu"  # neschimbat


def test_delete_proiect(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)

    resp = client.delete(f"/proiecte/{proiect_id}", headers=headers)
    assert resp.status_code == 204

    resp = client.get(f"/proiecte/{proiect_id}", headers=headers)
    assert resp.status_code == 404


def test_patch_tablou(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)
    tablou_id = _creeaza_tablou(client, headers, proiect_id)

    resp = client.patch(f"/tablouri/{tablou_id}", headers=headers, json={"nume": "TD1"})
    assert resp.status_code == 200
    assert resp.json()["nume"] == "TD1"


def test_delete_tablou_cascadeaza_circuite_si_receptori(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)
    tablou_id = _creeaza_tablou(client, headers, proiect_id)
    circuit_id = _creeaza_circuit(client, headers, tablou_id)
    _creeaza_receptor(client, headers, circuit_id)

    resp = client.delete(f"/tablouri/{tablou_id}", headers=headers)
    assert resp.status_code == 204

    assert client.get(f"/tablouri/{tablou_id}", headers=headers).status_code == 404
    assert client.get(f"/circuite/{circuit_id}", headers=headers).status_code == 404
    assert client.get(f"/circuite/{circuit_id}/receptori", headers=headers).status_code == 404


def test_patch_circuit(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)
    tablou_id = _creeaza_tablou(client, headers, proiect_id)
    circuit_id = _creeaza_circuit(client, headers, tablou_id)

    resp = client.patch(f"/circuite/{circuit_id}", headers=headers, json={"lungime_cablu_m": 25})
    assert resp.status_code == 200
    assert resp.json()["lungime_cablu_m"] == 25


def test_delete_circuit_cascadeaza_receptori(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)
    tablou_id = _creeaza_tablou(client, headers, proiect_id)
    circuit_id = _creeaza_circuit(client, headers, tablou_id)
    receptor_id = _creeaza_receptor(client, headers, circuit_id)

    resp = client.delete(f"/circuite/{circuit_id}", headers=headers)
    assert resp.status_code == 204

    assert client.get(f"/circuite/{circuit_id}", headers=headers).status_code == 404
    resp_patch = client.patch(
        f"/circuite/{circuit_id}/receptori/{receptor_id}", headers=headers, json={"nume": "x"}
    )
    assert resp_patch.status_code == 404


def test_patch_receptor(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)
    tablou_id = _creeaza_tablou(client, headers, proiect_id)
    circuit_id = _creeaza_circuit(client, headers, tablou_id)
    receptor_id = _creeaza_receptor(client, headers, circuit_id)

    resp = client.patch(
        f"/circuite/{circuit_id}/receptori/{receptor_id}", headers=headers, json={"putere_nominala_w": 100}
    )
    assert resp.status_code == 200
    assert resp.json()["putere_nominala_w"] == 100


def test_delete_receptor(client, auth_headers):
    headers = auth_headers()
    proiect_id = _creeaza_proiect(client, headers)
    tablou_id = _creeaza_tablou(client, headers, proiect_id)
    circuit_id = _creeaza_circuit(client, headers, tablou_id)
    receptor_id = _creeaza_receptor(client, headers, circuit_id)

    resp = client.delete(f"/circuite/{circuit_id}/receptori/{receptor_id}", headers=headers)
    assert resp.status_code == 204

    resp = client.get(f"/circuite/{circuit_id}/receptori", headers=headers)
    assert resp.json() == []
