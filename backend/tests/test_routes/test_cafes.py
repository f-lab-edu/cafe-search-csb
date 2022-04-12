import json

from utils import create_cafe
from utils import create_comment
from tests.conftest import admin_token_headers
from tests.conftest import normal_user_token_headers
from tests.conftest import other_user_token_headers


def test_read_cafe(client, admin_token_headers):
    create_cafe(client, admin_token_headers)
    response = client.get("/cafes/get/1")

    assert response.status_code == 200
    assert response.json()["cafename"] == "cafe1"


def test_read_all_cafes(client, admin_token_headers):
    datas = [
        {"cafename": "cafe1", "location": "testlocation1"},
        {"cafename": "cafe2", "location": "testlocation2"},
    ]
    for data in datas:
        client.post("/cafes/create", data=json.dumps(data), headers=admin_token_headers)
    response = client.get("cafes/all")
    print(response.json())

    assert response.status_code == 200
    assert response.json()[0]["cafename"] == "cafe1"
    assert response.json()[1]["cafename"] == "cafe2"


def test_update_cafe_success_by_admin(client, admin_token_headers):
    create_cafe(client, admin_token_headers)
    changed_cafe = {"cafename": "cafe2", "location": "testlocation"}
    response = client.post(
        "cafes/update/1", data=json.dumps(changed_cafe), headers=admin_token_headers
    )
    assert response.json()["msg"] == "Updated Successfully"


def test_update_cafe_fail_by_normal_user(
    client, normal_user_token_headers, admin_token_headers
):
    create_cafe(client, admin_token_headers)
    changed_cafe = {"cafename": "cafe2", "location": "testlocation"}
    response = client.post(
        "cafes/update/1",
        data=json.dumps(changed_cafe),
        headers=normal_user_token_headers,
    )
    assert response.status_code == 401


def test_delete_cafe_fail_by_user(
    client, normal_user_token_headers, admin_token_headers
):
    create_cafe(client, admin_token_headers)
    response = client.delete("/cafes/delete/1", headers=normal_user_token_headers)
    assert response.status_code == 401


def test_delete_cafe_success_by_admin(client, admin_token_headers):
    create_cafe(client, admin_token_headers)
    response = client.delete("/cafes/delete/1", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Deleted"


def test_read_comments(client, normal_user_token_headers, admin_token_headers):
    create_cafe(client, admin_token_headers)
    create_comment(client, normal_user_token_headers)
    response = client.get("cafes/1/comments", headers=normal_user_token_headers)

    assert response.status_code == 200
    assert response.json()[0]["comment"] == "Good!"


def test_delete_comment_success_by_same_user(
    client, normal_user_token_headers, admin_token_headers
):
    create_cafe(client, admin_token_headers)
    create_comment(client, normal_user_token_headers)
    response = client.delete(
        "cafes/comments/1/delete", headers=normal_user_token_headers
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Deleted"


def test_delete_comment_fail_by_other_user(
    client, admin_token_headers, normal_user_token_headers, other_user_token_headers
):
    create_cafe(client, admin_token_headers)
    create_comment(client, normal_user_token_headers)
    response = client.delete(
        "cafes/comments/1/delete", headers=other_user_token_headers
    )
    assert response.status_code == 401
