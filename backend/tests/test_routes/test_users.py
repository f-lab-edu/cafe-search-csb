import json


def test_create_user(client):
    data = {
        "username": "test-sbjo",
        "email": "testsb@jo.com",
        "password": "test-password",
    }
    response = client.post("/users/", data=json.dumps(data))
    assert response.status_code == 201
    assert response.json()["username"] == "test-sbjo"
    assert response.json()["email"] == "testsb@jo.com"
