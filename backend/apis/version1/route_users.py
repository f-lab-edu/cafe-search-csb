from db.session import get_db
from db.logics.users import create_new_user
from fastapi import APIRouter, Depends, status
from schemas.users import UserCreate, ShowUser
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
