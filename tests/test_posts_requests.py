from base64 import b64encode
from app import create_app

client = create_app().test_client()
client.application.testing = True
credentials = b64encode(b"username:password")

def test_get_method():
    unauth_response = client.get("/api/posts")
    assert unauth_response.status_code == 401

    get_response = client.get("/api/posts", headers={"Authorization": "Basic {}".format(credentials.decode())})
    assert get_response.status_code != 404
    assert get_response.status_code == 200
    assert isinstance(get_response.json, list)

def test_getbyid_method():
    unauth_response = client.get("/api/posts/1")
    assert unauth_response.status_code == 401

    getbyid_response = client.get("/api/posts/1",
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    if (getbyid_response.status_code != 404):
        assert getbyid_response.status_code == 200
    else:
        assert getbyid_response.status_code == 404

def test_post_method():
    payload = {
        "user_id": 1,
        "title": "test post",
        "body": "This is a test post"
    }

    unauth_response = client.post("/api/posts")
    assert unauth_response.status_code == 401

    post_response = client.post("/api/posts",
                                  json=payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    if (post_response.status_code != 404):
        assert post_response.status_code == 200
        assert post_response.json["id"] > 0
        assert post_response.json["user_id"] == payload["user_id"]
        assert post_response.json["title"] == payload["title"]
        assert post_response.json["body"] == payload["body"]

        client.delete("/api/posts/{}".format(post_response.json["id"]),
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    else:
        assert post_response.status_code == 404

def test_patch_method():
    payload = {
        "user_id": 1,
        "title": "test post",
        "body": "This is a test post"
    }

    unauth_response = client.patch("/api/posts/1")
    assert unauth_response.status_code == 401

    post_response = client.post("/api/posts",
                                  json=payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    if (post_response.json["id"] > 0):
        update_payload = {
            "title": "test post update",
        }
        updated_response = client.patch("/api/posts/{}".format(post_response.json["id"]),
                                  json=update_payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

        if (updated_response.json["id"] == post_response.json["id"]):
            assert updated_response.status_code == 200
            assert updated_response.json["title"] == update_payload["title"]
            assert updated_response.json["user_id"] == payload["user_id"]
            assert updated_response.json["body"] == payload["body"]

            client.delete("/api/posts/{}".format(updated_response.json["id"]),
                                    headers={"Authorization": "Basic {}".format(credentials.decode())})

    else:
        assert post_response.status_code == 404

def test_delete_method():
    payload = {
        "user_id": 1,
        "title": "test post",
        "body": "This is a test post"
    }

    unauth_response = client.patch("/api/posts/1")
    assert unauth_response.status_code == 401

    post_response = client.post("/api/posts",
                                  json=payload,
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

    id = post_response.json["id"]
    if ( id > 0):
        delete_response = client.delete("/api/posts/{}".format(id),
                                  headers={"Authorization": "Basic {}".format(credentials.decode())})

        assert delete_response.status_code == 204

    else:
        assert post_response.status_code == 404