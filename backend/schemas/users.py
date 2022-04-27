from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: bool = False


class ShowUser(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
