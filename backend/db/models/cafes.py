from sqlalchemy import Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.models.base import BaseMixin


cafe_ablefacility = Table(
    "cafe_ablefacility",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafe.id", ondelete="CASCADE")),
    Column("facility_id", ForeignKey("facility.id", ondelete="CASCADE")),
)


cafe_disablefacility = Table(
    "cafe_disablefacility",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafe.id", ondelete="CASCADE")),
    Column("facility_id", ForeignKey("facility.id", ondelete="CASCADE")),
)


cafe_tag = Table(
    "cafe_tag",
    Base.metadata,
    Column("cafe_id", ForeignKey("cafe.id", ondelete="CASCADE")),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE")),
)


class Cafe(Base, BaseMixin):
    cafename = Column(String(30), nullable=False)
    phone = Column(String(20))
    jibeonfullname = Column(String(150), nullable=False)
    dorofullname = Column(String(150), nullable=False)
    imageurl = Column(String(100))
    comments = relationship(
        "Comment",
        back_populates="cafe",
        cascade="all, delete",
        passive_deletes=True,
    )
    able_facilities = relationship(
        "Facility",
        secondary=cafe_ablefacility,
        back_populates="able_cafes",
        cascade="all, delete",
    )
    disable_facilities = relationship(
        "Facility",
        secondary=cafe_disablefacility,
        back_populates="disable_cafes",
        cascade="all, delete",
    )
    tags = relationship(
        "Tag",
        secondary=cafe_tag,
        back_populates="cafes",
        cascade="all, delete",
    )


class Comment(Base, BaseMixin):
    comment = Column(String(255), nullable=False)
    like = Column(Integer, nullable=False)
    cafeid = Column(Integer, ForeignKey("cafe.id", ondelete="CASCADE"))
    userid = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="comments")
    cafe = relationship("Cafe", back_populates="comments")


class Facility(Base, BaseMixin):
    name = Column(String(10), nullable=False)
    able_cafes = relationship(
        "Cafe",
        secondary=cafe_ablefacility,
        back_populates="able_facilities",
        passive_deletes=True,
    )
    disable_cafes = relationship(
        "Cafe",
        secondary=cafe_disablefacility,
        back_populates="disable_facilities",
        passive_deletes=True,
    )


class Tag(Base, BaseMixin):
    name = Column(String(10), nullable=False)
    cafes = relationship(
        "Cafe",
        secondary=cafe_tag,
        back_populates="tags",
        passive_deletes=True,
    )
