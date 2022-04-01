from operator import and_
from typing import List
from db.models.cafes import Cafe, Comment
from sqlalchemy import and_
from sqlalchemy.orm import Session


def get_cafe_by_id(id: int, db: Session):
    cafe = db.query(Cafe).filter(Cafe.id == id).first()
    if not cafe:
        return False
    return cafe


def search_cafe(cafename: str, location: str, db: Session) -> List[Cafe]:
    if not location:
        search = f"%{cafename}%"
        cafes = db.query(Cafe).filter(Cafe.cafename.like(search)).all()
        return cafes
    else:
        name_search = f"%{cafename}%"
        location_search = f"%{location}%"
        cafes = (
            db.query(Cafe)
            .filter(
                and_(
                    Cafe.cafename.like(name_search), Cafe.location.like(location_search)
                )
            )
            .all()
        )
        return cafes


def delete_cafe_by_id(id: int, db: Session):
    cafe = db.query(Cafe).filter(Cafe.id == id)
    if not cafe.first():
        return 0
    cafe.delete()
    db.commit()
    return 1


def create_comment(cafeid: int, userid: int, comment: str, db: Session):
    comment = Comment(**comment.dict(), cafeid=cafeid, userid=userid)
    db.add(comment)
    db.commit()
    return comment


def get_comment_by_id(commentid: int, db: Session):
    comment = db.query(Comment).filter(Comment.id == commentid).first()
    if not comment:
        return False
    return comment


def delete_comment_by_id(commentid: int, db: Session):
    comment = db.query(Comment).filter(Comment.id == commentid)
    comment.delete()
    db.commit()
    return
