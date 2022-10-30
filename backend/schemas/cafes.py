from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, constr, conint, validator


class CommentCreate(BaseModel):
    comment: constr(min_length=1, max_length=255)
    like: conint(gt=0, lt=5)


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
    cafename: constr(min_length=1, max_length=20)
    phone: Optional[constr(max_length=20)]
    jibeonfullname: constr(min_length=1, max_length=150)
    dorofullname: constr(min_length=1, max_length=150)
    imageurl: Optional[constr(max_length=100)]
    tags: Optional[str]
    able_facilities: List[Facility]
    disable_facilities: List[Facility]

    @validator("able_facilities", allow_reuse=True)
    def check_duplicate(cls, v):
        remove_duplicate = set(fac.value for fac in v)
        assert len(v) == len(remove_duplicate), "Facility Cannot Duplicated"

    @validator("disable_facilities", allow_reuse=True)
    def check_duplicate(cls, v):
        remove_duplicate = set(fac.value for fac in v)
        assert len(v) == len(remove_duplicate), "Facility Cannot Duplicated"

    @validator("tags")
    def check_tag_duplicate(cls, v):
        remove_duplicate = set(v.split())
        assert len(v) == len(remove_duplicate), "Tag Cannot Duplicated"


class CafeUpdate(BaseModel):
    cafename: Optional[constr(min_length=1, max_length=20)]
    phone: Optional[constr(max_length=20)]
    jibeonfullname: Optional[constr(min_length=1, max_length=150)]
    dorofullname: Optional[constr(min_length=1, max_length=150)]
    imageurl: Optional[constr(max_length=100)]
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
