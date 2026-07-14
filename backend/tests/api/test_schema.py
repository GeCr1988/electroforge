def test_schema_svg_status_si_content_type(client, auth_headers):
    headers = auth_headers()
    resp = client.post(
        "/proiecte",
        headers=headers,
        json={"nume": "Casa Ion", "beneficiar": "Ion", "tip_cladire": "rezidential", "tensiune_alimentare": "230/400V"},
    )
    proiect_id = resp.json()["id"]
    tablou_id = client.post(f"/proiecte/{proiect_id}/tablouri", headers=headers, json={"nume": "TE"}).json()["id"]
    client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C1 iluminat", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 10},
    )

    resp = client.get(f"/proiecte/{proiect_id}/schema-monofilara.svg", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/svg+xml"
    assert "TE" in resp.text
    assert "C1 iluminat" in resp.text


def test_schema_svg_necesita_ownership(client, auth_headers):
    headers_a = auth_headers(email="a@example.com")
    resp = client.post(
        "/proiecte",
        headers=headers_a,
        json={"nume": "P", "beneficiar": "B", "tip_cladire": "rezidential", "tensiune_alimentare": "230/400V"},
    )
    proiect_id = resp.json()["id"]

    headers_b = auth_headers(email="b@example.com")
    resp = client.get(f"/proiecte/{proiect_id}/schema-monofilara.svg", headers=headers_b)
    assert resp.status_code == 404
