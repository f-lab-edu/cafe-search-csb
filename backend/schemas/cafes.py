from typing import List, Tuple
from pydantic import BaseModel

class CommentCreate(BaseModel):
    comment: str
    like: int


class ShowComment(BaseModel):
    comment: str
    like: int

    class Config:
        orm_mode = True

class CafeCreate(BaseModel):
    cafename: str
    location: str


class ShowCafe(BaseModel):
    cafename: str
    location: str
    comments: List[ShowComment]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



