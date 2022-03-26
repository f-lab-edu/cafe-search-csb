from core.hashing import Hasher
from db.models.users import User
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session) -> User:
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(username: str, password: str, db: Session) -> User:
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user
