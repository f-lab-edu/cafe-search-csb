from typing import List
from pydantic import BaseModel


class Cafe(BaseModel):
    cafename: str
    location: str
    comments: List[str]


class CommentCreate(BaseModel):
    comment: str
    like: int


class ShowComment(BaseModel):
    comment: str
    like: int

    class Config:
        orm_mode = True
