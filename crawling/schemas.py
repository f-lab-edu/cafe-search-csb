from pydantic import BaseModel
from typing import Optional

class Cafe(BaseModel):
    address: Optional[str]
    phone: Optional[str]
    tags: list
    img_url: Optional[str]
    facilities: list
