def test_user_cannot_see_other_users_proiect(client, auth_headers):
    headers_a = auth_headers(email="a@example.com")
    resp = client.post(
        "/proiecte",
        headers=headers_a,
        json={
            "nume": "Casa A",
            "beneficiar": "Ion",
            "tip_cladire": "rezidential",
            "tensiune_alimentare": "230/400V",
        },
    )
    proiect_id = resp.json()["id"]

    headers_b = auth_headers(email="b@example.com")
    resp_get = client.get(f"/proiecte/{proiect_id}", headers=headers_b)
    assert resp_get.status_code == 404

    resp_list = client.get("/proiecte", headers=headers_b)
    assert resp_list.json() == []


def test_user_cannot_edit_other_users_proiect(client, auth_headers):
    headers_a = auth_headers(email="a@example.com")
    resp = client.post(
        "/proiecte",
        headers=headers_a,
        json={
            "nume": "Casa A",
            "beneficiar": "Ion",
            "tip_cladire": "rezidential",
            "tensiune_alimentare": "230/400V",
        },
    )
    proiect_id = resp.json()["id"]

    headers_b = auth_headers(email="b@example.com")
    resp_patch = client.patch(f"/proiecte/{proiect_id}", headers=headers_b, json={"nume": "Hacked"})
    assert resp_patch.status_code == 404

    resp_delete = client.delete(f"/proiecte/{proiect_id}", headers=headers_b)
    assert resp_delete.status_code == 404

    # proiectul userului A rămâne neatins
    resp_check = client.get(f"/proiecte/{proiect_id}", headers=headers_a)
    assert resp_check.status_code == 200
    assert resp_check.json()["nume"] == "Casa A"
