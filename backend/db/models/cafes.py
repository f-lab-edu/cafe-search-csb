from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.base import BaseMixin


cafe_ablefacility = Table(
    "cafe_ablefacility",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafe.id")),
    Column("facility_id", ForeignKey("facility.id"))
)

cafe_disablefacility = Table(
    "cafe_disablefacility",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafe.id")),
    Column("facility_id", ForeignKey("facility.id"))
)


cafe_tag = Table(
    "cafe_tag",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafe.id")),
    Column("tag_id", ForeignKey("tag.id"))
)


class Cafe(Base, BaseMixin):
    cafename = Column(String(20), nullable=False)
    phone=Column(String(20))
    jibeonfullname = Column(String(150), nullable=False)
    dorofullname = Column(String(150), nullable=False)
    imageurl = Column(String(100))
    comments = relationship("Comment", back_populates="cafe")
    able_facilities = relationship("Facility", secondary=cafe_ablefacility, back_populates="able_cafes")
    disable_facilities = relationship("Facility", secondary=cafe_disablefacility, back_populates="disable_cafes")
    tags = relationship("Tag", secondary=cafe_tag, back_populates="cafes")


class Comment(Base, BaseMixin):
    comment = Column(String(255), nullable=False)
    like = Column(Integer, nullable=False)
    cafeid = Column(Integer, ForeignKey("cafe.id"))
    userid = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="comments")
    cafe = relationship("Cafe", back_populates="comments")


class Facility(Base, BaseMixin):
    name = Column(String(10), nullable=False)
    able_cafes = relationship("Cafe", secondary=cafe_ablefacility, back_populates="able_facilities")
    disable_cafes = relationship("Cafe", secondary=cafe_disablefacility, back_populates="disable_facilities")


class Tag(Base, BaseMixin):
    name = Column(String(10), nullable=False)
    cafes = relationship("Cafe", secondary=cafe_tag, back_populates="tags")
