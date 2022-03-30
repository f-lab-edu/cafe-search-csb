from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any, Generator

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apis.base import api_router
from db.base import Base
from db.session import get_db
from core.config import settings


def start_application() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)
    return app


engine = create_engine(
    "mysql+pymysql://{username}:{password}@{host}:{port}/{name}?charset=utf8mb4".format(
        username=settings.TEST_DB_USERNAME,
        password=settings.TEST_DB_PASSWORD.get_secret_value(),
        host=settings.TEST_DB_HOST,
        port=settings.TEST_DB_PORT,
        name=settings.TEST_DB_NAME,
    )
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
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
