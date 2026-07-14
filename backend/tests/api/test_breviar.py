import pytest


def _weasyprint_disponibil() -> bool:
    try:
        from weasyprint import HTML  # noqa: F401

        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _weasyprint_disponibil(),
    reason="WeasyPrint indisponibil (lipsesc bibliotecile native Pango/GTK pe acest mediu) — "
    "verificat separat în Docker/CI, unde sunt instalate",
)


def test_breviar_pdf_status_si_content_type(client, auth_headers):
    headers = auth_headers()
    proiect_id = client.post(
        "/proiecte",
        headers=headers,
        json={"nume": "Casa Ion", "beneficiar": "Ion", "tip_cladire": "rezidential", "tensiune_alimentare": "230/400V"},
    ).json()["id"]
    tablou_id = client.post(f"/proiecte/{proiect_id}/tablouri", headers=headers, json={"nume": "TE"}).json()["id"]
    circuit_id = client.post(
        f"/tablouri/{tablou_id}/circuite",
        headers=headers,
        json={"nume": "C1", "tip": "monofazat", "mod_pozare": "B1", "lungime_cablu_m": 10},
    ).json()["id"]
    client.post(
        f"/circuite/{circuit_id}/receptori",
        headers=headers,
        json={"nume": "Bec", "tip": "iluminat", "putere_nominala_w": 100, "cos_phi": 1.0, "ku": 1.0, "ks": 1.0},
    )
    client.post(f"/circuite/{circuit_id}/calculeaza", headers=headers)

    resp = client.get(f"/proiecte/{proiect_id}/breviar.pdf", headers=headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content[:4] == b"%PDF"


def test_breviar_pdf_necesita_ownership(client, auth_headers):
    headers_a = auth_headers(email="a@example.com")
    proiect_id = client.post(
        "/proiecte",
        headers=headers_a,
        json={"nume": "P", "beneficiar": "B", "tip_cladire": "rezidential", "tensiune_alimentare": "230/400V"},
    ).json()["id"]

    headers_b = auth_headers(email="b@example.com")
    resp = client.get(f"/proiecte/{proiect_id}/breviar.pdf", headers=headers_b)
    assert resp.status_code == 404
