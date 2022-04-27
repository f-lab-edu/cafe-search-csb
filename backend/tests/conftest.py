from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, Generator

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apis.base import api_router
from db.base import Base
from db.session import get_db
from core.config import settings
from tests.utils import authentication_token_from_email


def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app


engine = create_engine(
    "mysql+pymysql://{username}:{password}@{host}:{port}/{name}?charset=utf8mb4".format(
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD.get_secret_value(),
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        name=settings.DB_NAME,
    )
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db_session: Session):
    return authentication_token_from_email(
        client=client, email=settings.TEST_USER_EMAIL, db=db_session, is_superuser=False
    )


@pytest.fixture(scope="function")
def admin_token_headers(client: TestClient, db_session: Session):
    return authentication_token_from_email(
        client=client, email=settings.TEST_ADMIN_EMAIL, db=db_session, is_superuser=True
    )


@pytest.fixture(scope="function")
def other_user_token_headers(client: TestClient, db_session: Session):
    return authentication_token_from_email(
        client=client,
        email=settings.TEST_SECOND_USER_EMAIL,
        db=db_session,
        is_superuser=False,
    )
