from utils import change_response, create_cafe, get_resp_with_json
import requests
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from config import settings
from db.base import Base
from db.session import engine, get_db


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    create_tables()
    return app


app = start_application()


@app.get("/scrap/{id}")
async def scrap_url(id: int, db: Session = Depends(get_db)) -> JSONResponse:
    try:
        resp = get_resp_with_json(id)
        if resp["status"] == "success":
            create_cafe(resp=resp, db=db)
        return JSONResponse(content=resp)
    except requests.RequestException:
        return JSONResponse(content={"status":"Fail"})
