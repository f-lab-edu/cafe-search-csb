from sqlalchemy import Column, String, Boolean

from db.base_class import Base
from db.models.base import BaseMixin


class User(Base, BaseMixin):
    username = Column(String(40), unique=True, nullable=False)
    email = Column(String(60), unique=True, nullable=False, index=True)
    hashed_password = Column(String(100), nullable=False)
    is_superuser = Column(Boolean(), default=False)
