from typing import List
from db.models.cafes import Cafe, Comment, Facility, Tag
from schemas.cafes import CafeCreate, CafeUpdate, CommentCreate
from sqlalchemy import and_
from sqlalchemy.orm import Session


def get_cafe_facility_tag_information(cafe: CafeCreate):
    cafe_information_dict = {}
    facility_information_dict = {}
    tags_list = []
    for k, v in cafe.dict().items():
        if k not in ("able_facilities", "disable_facilities", "tags") and v is not None:
            cafe_information_dict[k] = v
        elif k == "tags" and v is not None:
            tags_list = v.split(" ")
        elif k in ("able_facilities", "disable_facilities") and v is not None:
            facility_information_dict[k] = v
    return cafe_information_dict, facility_information_dict, tags_list


def make_new_cafe_for_db_add(
    cafe_information_dict, facility_information_dict, tags_list, db: Session
) -> Cafe:
    cafe_obj = Cafe(**cafe_information_dict)
    for facility in facility_information_dict["able_facilities"]:
        fac = db.query(Facility).filter(Facility.name == facility.value).first()
        if fac:
            cafe_obj.able_facilities.append(fac)
        else:
            fc = Facility(name=facility)
            cafe_obj.able_facilities.append(fc)
    for facility in facility_information_dict["disable_facilities"]:
        fac = db.query(Facility).filter(Facility.name == facility.value).first()
        if fac:
            cafe_obj.disable_facilities.append(fac)
        else:
            fc = Facility(name=facility)
            cafe_obj.disable_facilities.append(fc)
    for tag in tags_list:
        tg = db.query(Tag).filter(Tag.name == tag).first()
        if tg:
            cafe_obj.tags.append(tg)
        else:
            cafe_obj.tags.append(Tag(name=tag))
    return cafe_obj


def remove_existing_facility_then_add_new(facility_dict, db, existing_cafe):
    if facility_dict.get("able_facilities", ""):
        existing_able_facilities = (
            db.query(Facility).filter(Facility.able_cafes.contains(existing_cafe)).all()
        )
        for fac in existing_able_facilities:
            existing_cafe.able_facilities.remove(fac)

        for facility in facility_dict["able_facilities"]:
            fac = db.query(Facility).filter(Facility.name == facility.value).first()
            existing_cafe.able_facilities.append(fac)

    if facility_dict.get("disable_facilities", ""):
        existing_disable_facilities = (
            db.query(Facility)
            .filter(Facility.disable_cafes.contains(existing_cafe))
            .all()
        )
        for fac in existing_disable_facilities:
            existing_cafe.disable_facilities.remove(fac)

        for facility in facility_dict["disable_facilities"]:
            fac = db.query(Facility).filter(Facility.name == facility.value).first()
            existing_cafe.disable_facilities.append(fac)

    return existing_cafe


def remove_existing_tag_then_add_new(tags, db, existing_cafe):
    existing_tags = db.query(Tag).filter(Tag.cafes.contains(existing_cafe)).all()
    for tag in existing_tags:
        existing_cafe.tags.remove(tag)

    for tag_name in tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if tag:
            existing_cafe.tags.append(tag)
        else:
            tag = Tag(name=tag_name)
            existing_cafe.tags.append(tag)
    return existing_cafe


def create_new_cafe(cafe: CafeCreate, db: Session):
    cafe_dict, facility_dict, tags = get_cafe_facility_tag_information(cafe)
    cafe_obj = make_new_cafe_for_db_add(cafe_dict, facility_dict, tags, db)
    db.add(cafe_obj)
    db.commit()
    return cafe_obj


def get_cafe_by_id(id: int, db: Session):
    cafe = db.query(Cafe).filter(Cafe.id == id).first()
    if not cafe:
        return False
    return cafe


def get_all_cafes(limit: int, db: Session):
    cafes = db.query(Cafe).limit(limit).all()
    return cafes


def search_cafe(
    db: Session, limit: int, cafename: str = None, location: str = None
) -> List[Cafe]:
    name_search = f"%{cafename}%"
    loc_search = f"%{location}%"

    if cafename and location:
        cafes = (
            db.query(Cafe)
            .filter(
                and_(
                    Cafe.cafename.like(name_search),
                    Cafe.jibeonfullname.like(loc_search),
                )
            )
            .limit(limit)
            .all()
        )
    elif cafename and not location:
        cafes = (
            db.query(Cafe).filter(Cafe.cafename.like(name_search)).limit(limit).all()
        )
    elif not cafename and location:
        cafes = (
            db.query(Cafe)
            .filter(Cafe.jibeonfullname.like(loc_search))
            .limit(limit)
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


def update_cafe_by_id(id: int, cafe: CafeUpdate, db: Session):
    existing_cafe = db.query(Cafe).filter(Cafe.id == id)
    if not existing_cafe.first():
        return 0
    cafe_dict, facility_dict, tags = get_cafe_facility_tag_information(cafe)
    if cafe_dict:
        existing_cafe.update(cafe_dict)

    existing_cafe = existing_cafe.first()
    if tags:
        remove_existing_tag_then_add_new(tags, db, existing_cafe)

    if facility_dict:
        remove_existing_facility_then_add_new(facility_dict, db, existing_cafe)

    db.commit()
    return 1


def create_comment(cafeid: int, userid: int, comment: CommentCreate, db: Session):
    comment = Comment(**comment.dict(), cafeid=cafeid, userid=userid)
    db.add(comment)
    db.commit()
    return comment


def get_comments_by_cafeid(cafeid: int, db: Session):
    comments = db.query(Comment).filter(Comment.cafeid == cafeid).all()
    if not comments:
        return False
    return comments


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
