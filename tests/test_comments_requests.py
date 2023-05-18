from base64 import b64encode
from app import create_app

client = create_app().test_client()
client.application.testing = True
credentials = b64encode(b"username:password")

def test_get_method():
    unauth_response = client.get("/api/comments")
    assert unauth_response.status_code == 401

    get_response = client.get("/api/comments", headers={"Authorization": "Basic {}".format(credentials.decode())})
    assert get_response.status_code != 404
    assert get_response.status_code == 200
    assert isinstance(get_response.json, list)

def test_getbyid_method():
    unauth_response = client.get("/api/comments/1")
    assert unauth_response.status_code == 401

    getbyid_response = client.get("/api/comments/1",
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    if (getbyid_response.status_code != 404):
        assert getbyid_response.status_code == 200
    else:
        assert getbyid_response.status_code == 404

def test_post_method():
    payload = {
        "post_id": 1,
        "name": "test user",
        "body": "This is a test comment",
        "email": "email@example.com"
    }

    unauth_response = client.post("/api/comments")
    assert unauth_response.status_code == 401

    post_response = client.post("/api/comments",
                                  json=payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    if (post_response.status_code != 404):
        assert post_response.status_code == 200
        assert post_response.json["id"] > 0
        assert post_response.json["post_id"] == payload["post_id"]
        assert post_response.json["name"] == payload["name"]
        assert post_response.json["body"] == payload["body"]
        assert post_response.json["email"] == payload["email"]

        client.delete("/api/comments/{}".format(post_response.json["id"]),
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    else:
        assert post_response.status_code == 404

def test_patch_method():
    payload = {
        "post_id": 1,
        "name": "test user",
        "body": "This is a test comment",
        "email": "email@example.com"
    }

    unauth_response = client.patch("/api/comments/1")
    assert unauth_response.status_code == 401

    post_response = client.post("/api/comments",
                                  json=payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    if (post_response.json["id"] > 0):
        update_payload = {
            "name": "other user",
        }
        updated_response = client.patch("/api/comments/{}".format(post_response.json["id"]),
                                  json=update_payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

        if (updated_response.json["id"] == post_response.json["id"]):
            assert updated_response.status_code == 200
            assert updated_response.json["name"] == update_payload["name"]
            assert updated_response.json["post_id"] == payload["post_id"]
            assert updated_response.json["body"] == payload["body"]
            assert updated_response.json["email"] == payload["email"]

            client.delete("/api/comments/{}".format(updated_response.json["id"]),
                                    headers={"Authorization": "Basic {}".format(credentials.decode())})

    else:
        assert post_response.status_code == 404

def test_delete_method():
    payload = {
        "post_id": 1,
        "name": "test user",
        "body": "This is a test comment",
        "email": "email@example.com"
    }

    unauth_response = client.patch("/api/comments/1")
    assert unauth_response.status_code == 401

    post_response = client.post("/api/comments",
                                  json=payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    id = post_response.json["id"]
    if ( id > 0):
        delete_response = client.delete("/api/comments/{}".format(id),
                                        headers={"Authorization": "Basic {}".format(credentials.decode())})

        assert delete_response.status_code == 204

    else:
        assert post_response.status_code == 404

def test_get_comments_by_post_id():
    payload = {
        "user_id": 1,
        "title": "test post",
        "body": "This is a test post"
    }

    post_response = client.post("/api/posts",
                                json=payload,
                                headers={"Authorization": "Basic {}".format(credentials.decode())})

    post_id = post_response.json["id"]
    if (post_id > 0):
        comment_payload = {
            "post_id": post_id,
            "name": "test user",
            "body": "This is a test comment",
            "email": "email@example.com"
        }
        comment_payload2 = {
            "post_id": post_id,
            "name": "test user",
            "body": "This is a another comment",
            "email": "email@example.com"
        }

        comment_post_res = client.post("/api/comments",
                    json=comment_payload,
                    headers={"Authorization": "Basic {}".format(credentials.decode())})
        comment_post_res2 = client.post("/api/comments",
                    json=comment_payload2,
                    headers={"Authorization": "Basic {}".format(credentials.decode())})

        get_comments_res = client.get("/api/posts/{}/comments".format(post_id),
                                           headers={"Authorization": "Basic {}".format(credentials.decode())})

        assert isinstance(get_comments_res.json, list)
        assert comment_post_res.json in get_comments_res.json
        assert comment_post_res2.json in get_comments_res.json

        client.delete("/api/comments/{}".format(comment_post_res.json["id"]),
                                    headers={"Authorization": "Basic {}".format(credentials.decode())})
        client.delete("/api/comments/{}".format(comment_post_res2.json["id"]),
                                    headers={"Authorization": "Basic {}".format(credentials.decode())})
        client.delete("/api/posts/{}".format(post_id),
                                    headers={"Authorization": "Basic {}".format(credentials.decode())})