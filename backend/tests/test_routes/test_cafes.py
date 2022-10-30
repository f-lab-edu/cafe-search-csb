import json

from utils import create_single_cafe, create_multiple_cafe
from utils import create_single_comment, create_multiple_comment


def test_create_cafe_success_by_admin(client, admin_token_headers):
    response = create_single_cafe(client, admin_token_headers)
    assert response.status_code == 200
    assert response.json()["cafename"] == "카페방아"
    assert response.json()["tags"] == [{"name": "분위기좋은"}, {"name": "데이트코스"}]
    assert response.json()["able_facilities"] == [{"name": "흡연"}, {"name": "wifi"}]


def test_create_cafe_fail_validation_error(client, admin_token_headers):
    wrong_data = {
        "cafename": "",
        "phone": "02-222-2222",
        "jibeonfullname": "서울 동대문구 회기동 124-1",
        "dorofullname": "서울 동대문구 이문로 125",
        "imageurl": "",
        "tags": "분위기좋은 데이트코스",
        "able_facilities": ["흡연", "wifi"],
        "disable_facilities": ["주차"],
    }
    response = client.post(
        "/cafes", data=json.dumps(wrong_data), headers=admin_token_headers
    )
    assert response.status_code == 422


def test_create_cafe_fail_by_normal_user(client, normal_user_token_headers):
    response = create_single_cafe(client, normal_user_token_headers)
    assert response.status_code == 401


def test_read_cafe_success(client, admin_token_headers):
    create_single_cafe(client, admin_token_headers)
    response = client.get("/cafes/1")
    assert response.status_code == 200
    assert response.json()["cafename"] == "카페방아"


def test_read_all_cafes_success(client, admin_token_headers):
    create_multiple_cafe(client, admin_token_headers)
    response = client.get("/cafes")
    assert response.status_code == 200
    assert response.json()[0]["cafename"] == "카페방아"
    assert response.json()[1]["cafename"] == "커피정원"


def test_update_cafe_success_by_admin(client, admin_token_headers):
    create_single_cafe(client, admin_token_headers)
    changed_cafe = {"cafename": "슷하벅스", "able_facilities": ["주차", "wifi"]}
    update_response = client.post(
        "cafes/1", data=json.dumps(changed_cafe), headers=admin_token_headers
    )
    get_response = client.get("cafes/1")

    assert update_response.json()["msg"] == "Updated Successfully"
    assert get_response.json()["cafename"] == "슷하벅스"
    able_facilities = get_response.json()["able_facilities"]
    assert set(fac["name"] for fac in able_facilities) == set(("주차", "wifi"))


def test_update_cafe_fail_by_user(client, normal_user_token_headers):
    changed_cafe = {"cafename": "cafe2", "jibeonfullname": "testlocation"}
    response = client.post(
        "cafes/1",
        data=json.dumps(changed_cafe),
        headers=normal_user_token_headers,
    )
    assert response.status_code == 401


def test_update_cafe_fail_validation_error(client, admin_token_headers):
    create_single_cafe(client, admin_token_headers)
    changed_cafe = {"jibeonfullname": ""}
    response = client.post(
        "cafes/1", data=json.dumps(changed_cafe), headers=admin_token_headers
    )
    assert response.status_code == 422


def test_delete_cafe_fail_by_user(client, normal_user_token_headers):
    response = client.delete("/cafes/1", headers=normal_user_token_headers)
    assert response.status_code == 401


def test_delete_cafe_success_by_admin(
    client, admin_token_headers, normal_user_token_headers
):
    create_single_cafe(client, admin_token_headers)
    create_single_comment(client, normal_user_token_headers)
    response = client.delete("/cafes/1", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Deleted"


def test_add_comments_success_by_normal_user(
    client, admin_token_headers, normal_user_token_headers
):
    create_single_cafe(client, admin_token_headers)
    comment = {"comment": "Good", "like": 5}
    response = client.post(
        "cafes/1/comment", data=json.dumps(comment), headers=normal_user_token_headers
    )
    assert response.status_code == 201
    assert response.json()["comment"] == "Good"


def test_add_comments_fail_validation_error(
    client, admin_token_headers, normal_user_token_headers
):
    create_single_cafe(client, admin_token_headers)
    wrong_comment = {"comment": "", "like": 5}
    wrong_like = {"comment": "Good!", "like": 100}
    wrong_comment_response = client.post(
        "cafes/1/comment",
        data=json.dumps(wrong_comment),
        headers=normal_user_token_headers,
    )
    wrong_like_response = client.post(
        "cafes/1/comment",
        data=json.dumps(wrong_like),
        headers=normal_user_token_headers,
    )

    assert wrong_comment_response.status_code == 422
    assert wrong_like_response.status_code == 422


def test_read_comments(client, normal_user_token_headers, admin_token_headers):
    create_single_cafe(client, admin_token_headers)
    create_multiple_comment(client, normal_user_token_headers)
    response = client.get("cafes/1/comment", headers=normal_user_token_headers)

    assert response.status_code == 200
    assert response.json()[0]["comment"] == "Good!"
    assert response.json()[1]["comment"] == "Not Bad"


def test_delete_comment_success_by_same_user(
    client, normal_user_token_headers, admin_token_headers
):
    create_single_cafe(client, admin_token_headers)
    create_single_comment(client, normal_user_token_headers)
    response = client.delete("cafes/1/comment/1", headers=normal_user_token_headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Deleted"


def test_delete_comment_fail_by_other_user(
    client, admin_token_headers, normal_user_token_headers, other_user_token_headers
):
    create_single_cafe(client, admin_token_headers)
    create_single_comment(client, normal_user_token_headers)
    response = client.delete("cafes/1/comment/1", headers=other_user_token_headers)
    assert response.status_code == 401
