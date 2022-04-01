from typing import List, Optional
from apis.version1.route_login import get_current_user_from_token
from db.session import get_db
from db.models.users import User
from db.logics.cafes import (
    search_cafe,
    get_cafe_by_id,
    delete_cafe_by_id,
    create_comment,
    get_comment_by_id,
    delete_comment_by_id,
)
from fastapi import APIRouter, Depends, HTTPException, status

from schemas.cafes import Cafe, CommentCreate, ShowComment
from sqlalchemy.orm import Session

router = APIRouter()


class LimitParams:
    def __init__(self, offset: int = 0, limit: int = 5):
        self.offset = offset
        self.limit = limit


@router.get("/", response_model=List[Cafe])
def searching_cafe(
    cafename: str = None,
    location: str = None,
    db: Session = Depends(get_db),
    params: LimitParams = Depends(LimitParams),
):
    if not cafename and not location:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must Input Cafe Name or Location",
        )
    cafes = search_cafe(cafename, location, db)
    if not cafes:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't find Cafe",
        )
    return cafes[params.offest : params.offset + params.limit]


@router.delete("/delete/{id}")
def delete_cafe(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superuser:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only Admin can delete cafe",
        )

    result = delete_cafe_by_id(id=id, db=db)
    if not result:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Can't Find Cafe"
        )
    return {"msg": "Deleted"}


@router.post("/{cafeid}/comment", response_model=ShowComment)
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


@router.delete("/comments/{commentid}/delete")
def delete_comment(
    commentid: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    comment = get_comment_by_id(commentid=commentid, db=db)
    if not comment:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Can't Find Comment"
        )
    if comment.userid != current_user.id:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Can't Delete Other's Comment",
        )
    delete_comment_by_id(commentid=commentid, userid=current_user.id, db=db)
    return {"msg": "Deleted"}
