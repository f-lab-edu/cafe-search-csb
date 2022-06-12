from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine
from middlewares.custom_logger import access_control

import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware



def include_router(app: FastAPI):
    app.include_router(api_router)

def add_middleware(app: FastAPI):
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)

def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    add_middleware(app)
    include_router(app)
    create_tables()
    return app


app = start_application()
