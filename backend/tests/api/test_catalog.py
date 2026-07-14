def test_creeaza_si_listeaza_componenta(client, auth_headers):
    headers = auth_headers()
    resp = client.post(
        "/catalog",
        headers=headers,
        json={
            "categorie": "protectie",
            "nume": "Disjunctor C16",
            "specificatii": {"in_a": 16, "curba": "C", "icu_ka": 6},
            "pret_estimativ": 25.0,
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["categorie"] == "protectie"
    assert body["unitate_masura"] == "buc"

    resp = client.get("/catalog", headers=headers)
    assert len(resp.json()) == 1


def test_filtreaza_catalog_dupa_categorie(client, auth_headers):
    headers = auth_headers()
    client.post("/catalog", headers=headers, json={"categorie": "protectie", "nume": "P1"})
    client.post("/catalog", headers=headers, json={"categorie": "cablu", "nume": "C1"})

    resp = client.get("/catalog?categorie=cablu", headers=headers)
    body = resp.json()
    assert len(body) == 1
    assert body[0]["nume"] == "C1"


def test_patch_si_delete_componenta(client, auth_headers):
    headers = auth_headers()
    resp = client.post("/catalog", headers=headers, json={"categorie": "protectie", "nume": "P1"})
    componenta_id = resp.json()["id"]

    resp = client.patch(f"/catalog/{componenta_id}", headers=headers, json={"pret_estimativ": 99.0})
    assert resp.status_code == 200
    assert resp.json()["pret_estimativ"] == 99.0

    resp = client.delete(f"/catalog/{componenta_id}", headers=headers)
    assert resp.status_code == 204
    assert client.get(f"/catalog/{componenta_id}", headers=headers).status_code == 404


def test_catalog_izolat_pe_utilizator(client, auth_headers):
    headers_a = auth_headers(email="a@example.com")
    resp = client.post("/catalog", headers=headers_a, json={"categorie": "protectie", "nume": "P1"})
    componenta_id = resp.json()["id"]

    headers_b = auth_headers(email="b@example.com")
    assert client.get(f"/catalog/{componenta_id}", headers=headers_b).status_code == 404
    assert client.get("/catalog", headers=headers_b).json() == []


def test_circuit_patch_seteaza_protectie_manual_si_dezactiveaza_auto(client, auth_headers):
    headers = auth_headers()
    resp = client.post(
        "/proiecte",
        headers=headers,
        json={"nume": "P", "beneficiar": "B", "tip_cladire": "rezidential", "tensiune_alimentare": "230/400V"},
    )
    proiect_id = resp.json()["id"]
    tablou_id = client.post(f"/proiecte/{proiect_id}/tablouri", headers=headers, json={"nume": "TE"}).json()["id"]
    circuit_id = client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C1", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 10},
    ).json()["id"]

    assert client.get(f"/circuite/{circuit_id}", headers=headers).json()["protectie_auto"] is True

    componenta_id = client.post(
        "/catalog", headers=headers, json={"categorie": "protectie", "nume": "C16"}
    ).json()["id"]

    resp = client.patch(
        f"/circuite/{circuit_id}", headers=headers, json={"protectie_selectata_id": componenta_id}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["protectie_selectata_id"] == componenta_id
    assert body["protectie_auto"] is False
