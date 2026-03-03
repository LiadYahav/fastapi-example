def test_get_posts_unauthorized(client):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_posts_empty(authorized_client):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert res.json() == []


def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_get_posts_limit(authorized_client, test_posts):
    res = authorized_client.get("/posts/?limit=2")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_get_posts_search(authorized_client, test_posts):
    res = authorized_client.get("/posts/?search=First")
    assert res.status_code == 200
    results = res.json()
    assert len(results) == 1
    assert results[0]["Post"]["title"] == "First Post"


def test_create_post(authorized_client):
    res = authorized_client.post("/posts/", json={"title": "My Post", "content": "Some content"})
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "My Post"
    assert body["content"] == "Some content"
    assert body["published"] is True
    assert "id" in body
    assert "owner" in body


def test_create_post_unpublished(authorized_client):
    res = authorized_client.post(
        "/posts/",
        json={"title": "Draft", "content": "Draft content", "published": False},
    )
    assert res.status_code == 201
    assert res.json()["published"] is False


def test_create_post_unauthorized(client):
    res = client.post("/posts/", json={"title": "Bad", "content": "Bad"})
    assert res.status_code == 401


def test_get_post(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    res = authorized_client.get(f"/posts/{post_id}")
    assert res.status_code == 200
    body = res.json()
    assert body["Post"]["id"] == post_id
    assert "votes" in body


def test_get_post_not_found(authorized_client):
    res = authorized_client.get("/posts/999999")
    assert res.status_code == 404


def test_update_post(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    res = authorized_client.put(
        f"/posts/{post_id}",
        json={"title": "Updated Title", "content": "Updated content", "published": True},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["title"] == "Updated Title"
    assert body["content"] == "Updated content"


def test_update_post_not_found(authorized_client):
    res = authorized_client.put(
        "/posts/999999",
        json={"title": "X", "content": "X", "published": True},
    )
    assert res.status_code == 404


def test_update_post_other_user(client, test_user2, test_posts):
    login = client.post(
        "/login",
        data={"username": test_user2["email"], "password": test_user2["password"]},
    )
    token = login.json()["access_token"]
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    post_id = test_posts[0]["id"]
    res = client.put(
        f"/posts/{post_id}",
        json={"title": "Hacked", "content": "Hacked", "published": True},
    )
    assert res.status_code == 403


def test_delete_post(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 204


def test_delete_post_not_found(authorized_client):
    res = authorized_client.delete("/posts/999999")
    assert res.status_code == 404


def test_delete_post_other_user(client, test_user2, test_posts):
    login = client.post(
        "/login",
        data={"username": test_user2["email"], "password": test_user2["password"]},
    )
    token = login.json()["access_token"]
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    post_id = test_posts[0]["id"]
    res = client.delete(f"/posts/{post_id}")
    assert res.status_code == 403


def test_delete_post_unauthorized(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0]['id']}")
    assert res.status_code == 401
