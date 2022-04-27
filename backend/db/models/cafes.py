from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.base import BaseMixin


class Cafe(Base, BaseMixin):
    cafename = Column(String(20), nullable=False)
    location = Column(String(50), nullable=False)
    comments = relationship("Comment", back_populates="cafe")


class Comment(Base, BaseMixin):
    comment = Column(String(255), nullable=False)
    like = Column(Integer, nullable=False)
    cafeid = Column(Integer, ForeignKey("cafe.id"))
    userid = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="comments")
    cafe = relationship("Cafe", back_populates="comments")
