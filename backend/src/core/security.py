from typing import Any, Dict
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from uuid import UUID
from .config import AUTH_SECRET_KEY, AUTH_ALGORITHM
from src.models import User
import jwt

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return password_hash.hash(plain_password)


def create_access_token(uuid: UUID, expire_time: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expire_time
    to_encode: dict[str, Any] = {"expiration": expire.timestamp(), "uuid": str(uuid)}
    assert AUTH_SECRET_KEY is not None, "AUTH_SECRET_KEY must be set"
    return jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)  # type: ignore


def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])  # type: ignore
        return payload
    except jwt.exceptions.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    access_token_cookie: str | None = Cookie(default=None, alias="access_token"),
    db: Session = Depends(get_db),
) -> User:
    token_to_use = token or access_token_cookie

    if not token_to_use:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    if token_to_use.lower().startswith("bearer "):
        token_to_use = token_to_use.split(" ", 1)[1].strip()

    payload = decode_access_token(token_to_use)
    user_uuid = payload.get("uuid")

    if not user_uuid:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
