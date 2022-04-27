from typing import List
from pydantic import BaseModel


class CafeCreate(BaseModel):
    cafename: str
    location: str


class ShowCafe(BaseModel):
    cafename: str
    location: str
    comments: List[str]

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    comment: str
    like: int


class ShowComment(BaseModel):
    comment: str
    like: int

    class Config:
        orm_mode = True
