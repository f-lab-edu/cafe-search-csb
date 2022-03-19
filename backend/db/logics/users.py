from db.models.users import User
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
