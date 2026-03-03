def test_create_user(client):
    res = client.post("/users/", json={"email": "newuser@example.com", "password": "password123"})
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "newuser@example.com"
    assert "id" in body
    assert "created_at" in body
    assert "password" not in body


def test_create_user_duplicate_email(client):
    data = {"email": "dup@example.com", "password": "pass123"}
    client.post("/users/", json=data)
    res = client.post("/users/", json=data)
    assert res.status_code == 409


def test_create_user_invalid_email(client):
    res = client.post("/users/", json={"email": "not-an-email", "password": "pass123"})
    assert res.status_code == 422


def test_get_user(authorized_client, test_user):
    res = authorized_client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200
    body = res.json()
    assert body["id"] == test_user["id"]
    assert body["email"] == test_user["email"]


def test_get_user_not_found(authorized_client):
    res = authorized_client.get("/users/999999")
    assert res.status_code == 404


def test_get_user_unauthorized(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 401


def test_get_all_users(authorized_client, test_user, test_user2):
    res = authorized_client.get("/users/")
    assert res.status_code == 200
    assert len(res.json()) >= 2
