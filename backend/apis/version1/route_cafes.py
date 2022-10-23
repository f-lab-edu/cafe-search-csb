from typing import List, Optional
from apis.version1.route_login import get_current_user_from_token
from db.session import get_db
from db.models.users import User
from db.logics.cafes import (
    create_new_cafe,
    search_cafe,
    get_cafe_by_id,
    get_all_cafes,
    delete_cafe_by_id,
    create_comment,
    get_comments_by_cafeid,
    get_comment_by_id,
    delete_comment_by_id,
    update_cafe_by_id,
)
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.cafes import CafeCreate, CafeUpdate, ShowCafe, CommentCreate, ShowComment
from sqlalchemy.orm import Session

router = APIRouter()


class LimitParams:
    def __init__(self, offset: int = 0, limit: int = 5):
        self.offset = offset
        self.limit = limit


@router.get("", response_model=List[ShowCafe])
def read_cafes(
    db: Session = Depends(get_db), params: LimitParams = Depends(LimitParams)
):
    cafes = get_all_cafes(db=db, limit=params.limit)
    return cafes


@router.post("", response_model=ShowCafe)
def create_cafe(
    cafe: CafeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Only Admin can Create Cafe",
        )
    cafe = create_new_cafe(cafe=cafe, db=db)
    return cafe


@router.post("/search", response_model=List[ShowCafe])
def searching_cafe(
    cafename: str = None,
    location: str = None,
    db: Session = Depends(get_db),
    params: LimitParams = Depends(LimitParams)
):
    if not cafename and not location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must Input Cafe Name or Location",
        )
    cafes = search_cafe(db, params.limit,cafename=cafename,location=location)
    if not cafes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find Cafe",
        )
    return cafes

@router.get("/{id}", response_model=ShowCafe)
def read_cafe(id: int, db: Session = Depends(get_db)):
    cafe = get_cafe_by_id(id=id, db=db)
    if not cafe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cafe with this ID {id} does not exist",
        )
    return cafe


@router.post("/{id}")
def update_cafe(
    id: int,
    cafe: CafeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    print("Current User : ", current_user.is_superuser)
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only Admin can update cafe info",
        )
    msg = update_cafe_by_id(id=id, cafe=cafe, db=db)
    if not msg:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Cafe with Id {id} not found"
        )
    return {"msg": "Updated Successfully"}


@router.delete("/{id}")
def delete_cafe(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only Admin can delete cafe",
        )

    result = delete_cafe_by_id(id=id, db=db)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Can't Find Cafe"
        )
    return {"msg": "Deleted"}


@router.post(
    "/{cafeid}/comment", response_model=ShowComment, status_code=status.HTTP_201_CREATED
)
def add_comment(
    cafeid: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    comment = create_comment(
        cafeid=cafeid, userid=current_user.id, comment=comment, db=db
    )
    return comment


@router.get("/{cafeid}/comment", response_model=List[ShowComment])
def read_comments(
    cafeid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    comments = get_comments_by_cafeid(cafeid=cafeid, db=db)
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Can't Find Comment"
        )
    return comments


@router.delete("/comments/{commentid}/delete")
def delete_comment(
    commentid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    comment = get_comment_by_id(commentid=commentid, db=db)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Can't Find Comment"
        )
    if comment.userid != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Can't Delete Other's Comment",
        )
    delete_comment_by_id(commentid=commentid, db=db)
    return {"msg": "Deleted"}
