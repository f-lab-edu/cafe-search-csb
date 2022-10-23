from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class CommentCreate(BaseModel):
    comment: str
    like: int


class ShowComment(BaseModel):
    comment: str
    like: int

    class Config:
        orm_mode = True


class ShowFacility(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ShowTag(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Facility(str, Enum):
    smokingromm = "흡연"
    fordisabled = "장애인시설"
    nuersery = "놀이방"
    parking = "주차"
    wifi = "wifi"
    pet = "애완동물출입"


class CafeCreate(BaseModel):
    cafename: str
    phone: Optional[str]
    jibeonfullname: str
    dorofullname: str
    imageurl: Optional[str]
    tags: Optional[str]
    able_facilities: List[Facility]
    disable_facilities: List[Facility]


class CafeUpdate(BaseModel):
    cafename: Optional[str]
    phone: Optional[str]
    jibeonfullname: Optional[str]
    dorofullname: Optional[str]
    imageurl: Optional[str]
    tags: Optional[str]
    able_facilities: Optional[List[Facility]]
    disable_facilities: Optional[List[Facility]]


class ShowCafe(BaseModel):
    cafename: str
    phone: str
    jibeonfullname: str
    dorofullname: str
    comments: List[ShowComment]
    able_facilities: List[ShowFacility]
    disable_facilities: List[ShowFacility]
    tags: List[ShowTag]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
