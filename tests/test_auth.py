import jwt

from app.config import settings


def test_login_success(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["token_type"] == "bearer"
    assert "access_token" in body


def test_login_returns_valid_jwt(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    token = res.json()["access_token"]
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    assert str(test_user["id"]) == payload.get("sub")


def test_login_wrong_password(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": "wrongpassword"},
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid Credentials"


def test_login_wrong_email(client, test_user):
    res = client.post(
        "/login",
        data={"username": "nobody@example.com", "password": test_user["password"]},
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid Credentials"


def test_login_missing_fields(client):
    res = client.post("/login", data={})
    assert res.status_code == 422
