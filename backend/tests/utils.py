import json
from db.logics.users import authenticate_user
from db.logics.users import create_new_user
from fastapi.testclient import TestClient
from schemas.users import UserCreate
from sqlalchemy.orm import Session
from core.config import settings
from typing import Dict


def user_authentication_headers(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    response = client.post("/login/token", data=data).json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
    client: TestClient, email: str, db: Session, is_superuser: bool
):
    password = settings.TEST_USER_PASSWORD
    user = authenticate_user(username=email, password=password, db=db)
    if not user:
        user_in_create = UserCreate(
            username=email, email=email, password=password, is_superuser=is_superuser
        )
        user = create_new_user(user=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)


def create_single_cafe(client: TestClient, headers: Dict[str, str]):
    data = {
        "cafename": "카페방아",
        "phone": "02-222-2222",
        "jibeonfullname": "서울 동대문구 회기동 124-1",
        "dorofullname": "서울 동대문구 이문로 125",
        "imageurl": "",
        "tags": "분위기좋은 데이트코스",
        "able_facilities": ["흡연", "wifi"],
        "disable_facilities": ["주차"],
    }
    response = client.post("/cafes", data=json.dumps(data), headers=headers)
    return response


def create_multiple_cafe(client: TestClient, headers: Dict[str, str]):
    datas = [
        {
            "cafename": "카페방아",
            "phone": "02-222-2222",
            "jibeonfullname": "서울 동대문구 회기동 124-1",
            "dorofullname": "서울 동대문구 이문로 125",
            "imageurl": "",
            "tags": "분위기좋은 데이트코스",
            "able_facilities": ["흡연", "wifi"],
            "disable_facilities": ["주차"],
        },
        {
            "cafename": "커피정원",
            "phone": "02-333-3333",
            "jibeonfullname": "서울 마포구 망원동 425-33",
            "dorofullname": "서울 마포구 망원로 7길 31-14",
            "imageurl": "www.www.www.",
            "tags": "로스팅카페",
            "able_facilities": ["주차", "wifi"],
            "disable_facilities": ["놀이방", "흡연"],
        },
    ]
    for data in datas:
        client.post("/cafes", data=json.dumps(data), headers=headers)


def create_single_comment(client: TestClient, headers: Dict[str, str]):
    data = {"comment": "Good!", "like": 5}
    client.post("/cafes/1/comment", data=json.dumps(data), headers=headers)


def create_multiple_comment(client: TestClient, headers: Dict[str, str]):
    datas = [{"comment": "Good!", "like": 5}, {"comment": "Not Bad", "like": 3}]
    for data in datas:
        client.post("cafes/1/comment", data=json.dumps(data), headers=headers)
