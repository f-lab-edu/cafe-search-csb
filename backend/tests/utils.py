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


def create_cafe(client: TestClient, headers: Dict[str, str]):
    data = {"cafename": "cafe1", "location": "testlocation"}
    client.post("/cafes/create", data=json.dumps(data), headers=headers)


def create_comment(client: TestClient, headers: Dict[str, str]):
    data = {"comment": "Good!", "like": 5}
    client.post("/cafes/1/comment", data=json.dumps(data), headers=headers)
