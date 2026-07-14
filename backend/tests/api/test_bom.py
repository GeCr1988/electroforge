def _proiect_cu_doua_circuite_folosind_acelasi_cablu(client, headers):
    proiect_id = client.post(
        "/proiecte",
        headers=headers,
        json={"nume": "P", "beneficiar": "B", "tip_cladire": "rezidential", "tensiune_alimentare": "230/400V"},
    ).json()["id"]
    tablou_id = client.post(f"/proiecte/{proiect_id}/tablouri", headers=headers, json={"nume": "TE"}).json()["id"]

    cablu_id = client.post(
        "/catalog", headers=headers, json={"categorie": "cablu", "nume": "FY 1.5", "pret_estimativ": 2.0}
    ).json()["id"]
    protectie_id = client.post(
        "/catalog", headers=headers, json={"categorie": "protectie", "nume": "C16", "pret_estimativ": 25.0}
    ).json()["id"]

    circuit1_id = client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C1", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 10},
    ).json()["id"]
    circuit2_id = client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C2", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 20},
    ).json()["id"]

    for cid in (circuit1_id, circuit2_id):
        client.patch(
            f"/circuite/{cid}",
            headers=headers,
            json={"cablu_selectat_id": cablu_id, "protectie_selectata_id": protectie_id},
        )

    return proiect_id


def test_bom_sumeaza_acelasi_cablu_pe_circuite_diferite(client, auth_headers):
    headers = auth_headers()
    proiect_id = _proiect_cu_doua_circuite_folosind_acelasi_cablu(client, headers)

    resp = client.get(f"/proiecte/{proiect_id}/bom", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    linii = {l["nume"]: l for l in body["linii"]}

    assert linii["FY 1.5"]["cantitate_totala"] == 30  # 10 + 20
    assert linii["FY 1.5"]["cost_total"] == 60.0  # 30 * 2.0
    assert linii["C16"]["cantitate_totala"] == 2  # cate 1 pe fiecare circuit
    assert linii["C16"]["cost_total"] == 50.0

    assert body["cost_total_general"] == 110.0


def test_bom_csv_contine_header_si_linii(client, auth_headers):
    headers = auth_headers()
    proiect_id = _proiect_cu_doua_circuite_folosind_acelasi_cablu(client, headers)

    resp = client.get(f"/proiecte/{proiect_id}/bom.csv", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/csv")
    assert "FY 1.5" in resp.text
    assert "Total general" in resp.text


def test_bom_gol_pentru_proiect_fara_selectii(client, auth_headers):
    headers = auth_headers()
    proiect_id = client.post(
        "/proiecte",
        headers=headers,
        json={"nume": "P", "beneficiar": "B", "tip_cladire": "rezidential", "tensiune_alimentare": "230/400V"},
    ).json()["id"]

    resp = client.get(f"/proiecte/{proiect_id}/bom", headers=headers)
    assert resp.json() == {"linii": [], "cost_total_general": 0.0}
