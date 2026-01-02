from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr, BaseModel, Field, model_validator
from datetime import timedelta
from uuid import UUID
from src.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.models import User
from src.core import security
from src.core.config import (
    MIN_FIRST_NAME_LENGTH,
    MIN_LAST_NAME_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
    MAX_EMAIL_LENGTH,
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    ACCESS_TOKEN_EXPIRE_TIME_DAYS,
)

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=MAX_EMAIL_LENGTH)
    password: str = Field(
        min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH
    )
    password_confirm: str
    first_name: str = Field(
        min_length=MIN_FIRST_NAME_LENGTH, max_length=MAX_FIRST_NAME_LENGTH
    )
    last_name: str = Field(
        min_length=MIN_LAST_NAME_LENGTH, max_length=MAX_LAST_NAME_LENGTH
    )

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords must match.")
        return self


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


@router.post("/register/", response_model=AuthResponse)
async def register_user(
    user_info: UserCreate, db: Session = Depends(get_db)
) -> AuthResponse:
    password_hashed = security.get_password_hash(user_info.password)

    new_user = User(
        email=user_info.email.lower(),
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        password_hash=password_hashed,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        print(f"Integrity Error details: {error_message}")
        raise HTTPException(status_code=400, detail="Account already exists.")

    generated_token = security.create_access_token(
        new_user.id, timedelta(days=ACCESS_TOKEN_EXPIRE_TIME_DAYS)
    )

    return AuthResponse(
        access_token=generated_token,
        user=UserOut(
            id=new_user.id,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
        ),
    )


@router.post("/login/", response_model=AuthResponse)
async def login_user(user: UserLogin):
    pass


@router.get("/me/", response_model=UserOut)
async def me():
    pass
