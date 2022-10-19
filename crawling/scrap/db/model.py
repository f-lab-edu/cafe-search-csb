from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base import Base, BaseMixin


cafe_facility = Table(
    "cafe_facility",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafe.id")),
    Column("facility_id", ForeignKey("facility.id"))
)


class Cafe(Base, BaseMixin):
    cafename = Column(String(20), nullable=False)
    phone=Column(String(20))
    jibeonfullname = Column(String(150), nullable=False)
    dorofullname = Column(String(150), nullable=False)
    imageurl = Column(String(100))
    tags = Column(String(100))
    comments = relationship("Comment", back_populates="cafe")
    able_facilities = relationship("Facility", secondary=cafe_facility, back_populates="cafes")
    disable_facilities = relationship("Facility", secondary=cafe_facility, back_populates="cafes")


class Comment(Base, BaseMixin):
    comment = Column(String(255), nullable=False)
    like = Column(Integer, nullable=False)
    cafeid = Column(Integer, ForeignKey("cafe.id"))
    userid = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="comments")
    cafe = relationship("Cafe", back_populates="comments")


class Facility(Base, BaseMixin):
    name = Column(String(10), nullable=False)
    cafes = relationship("Cafe", secondary=cafe_facility, back_populates="facilities")
