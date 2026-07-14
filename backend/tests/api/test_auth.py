def test_register_success(client):
    resp = client.post("/auth/register", json={"email": "a@example.com", "password": "parola123"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "a@example.com"
    assert body["rol"] == "proiectant"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "a@example.com", "password": "parola123"})
    resp = client.post("/auth/register", json={"email": "a@example.com", "password": "altaparola"})
    assert resp.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={"email": "a@example.com", "password": "parola123"})
    resp = client.post("/auth/login", data={"username": "a@example.com", "password": "parola123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "a@example.com", "password": "parola123"})
    resp = client.post("/auth/login", data={"username": "a@example.com", "password": "gresita"})
    assert resp.status_code == 401


def test_me_requires_token(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401


def test_me_with_token(client, auth_headers):
    headers = auth_headers()
    resp = client.get("/auth/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "user@example.com"
