from apis.version1.route_login import get_current_user_from_token
from db.session import get_db
from db.models.users import User
from db.logics.users import create_new_user, delete_user
from fastapi import APIRouter, Depends, status
from schemas.users import UserCreate, ShowUser
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.delete("/")
def delete_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    delete_user(user=current_user, db=db)
    return {"msg": "Deleted"}
