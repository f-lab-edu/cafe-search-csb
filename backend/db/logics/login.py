from core.config import settings
from datetime import datetime, timedelta
from jose import jwt
from typing import Dict, Optional


def create_access_token(
    data: Dict[str, str], expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if not expires_delta:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.SECRET_ALGORITHM
    )
    return encoded_jwt
