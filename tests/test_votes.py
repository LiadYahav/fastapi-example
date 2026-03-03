def test_vote_on_post(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    res = authorized_client.post("/vote/", json={"post_id": post_id, "direction": 1})
    assert res.status_code == 201


def test_vote_twice_on_same_post(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    authorized_client.post("/vote/", json={"post_id": post_id, "direction": 1})
    res = authorized_client.post("/vote/", json={"post_id": post_id, "direction": 1})
    assert res.status_code == 409


def test_remove_vote(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    authorized_client.post("/vote/", json={"post_id": post_id, "direction": 1})
    res = authorized_client.post("/vote/", json={"post_id": post_id, "direction": 0})
    assert res.status_code == 204


def test_remove_vote_not_exists(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    res = authorized_client.post("/vote/", json={"post_id": post_id, "direction": 0})
    assert res.status_code == 404


def test_vote_nonexistent_post(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 999999, "direction": 1})
    assert res.status_code == 404


def test_vote_unauthorized(client, test_posts):
    post_id = test_posts[0]["id"]
    res = client.post("/vote/", json={"post_id": post_id, "direction": 1})
    assert res.status_code == 401


def test_vote_reflected_in_post(authorized_client, test_posts):
    post_id = test_posts[0]["id"]
    authorized_client.post("/vote/", json={"post_id": post_id, "direction": 1})
    res = authorized_client.get(f"/posts/{post_id}")
    assert res.status_code == 200
    assert res.json()["votes"] == 1
