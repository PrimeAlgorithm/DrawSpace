from typing import List
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.database import get_db
from src.models.boards import Board
from src.models.users import User
from src.core import security


router = APIRouter()


class BoardIn(BaseModel):
    name: str


class BoardOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=List[BoardOut])
async def get_boards(
    user: User = Depends(security.get_current_user), db: Session = Depends(get_db)
) -> List[Board]:
    try:
        result = db.query(Board).filter_by(user_id=user.id).all()
        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        print(f"Database error during login: {e}")
        raise HTTPException(status_code=500, detail="A database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal server error occurred")


@router.post("/", response_model=BoardOut)
async def create_board(
    board_details: BoardIn,
    user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> Board:
    new_board = Board(
        user_id=user.id, name=board_details.name, properties={}, elements=[]
    )

    try:
        db.add(new_board)
        db.commit()
        db.refresh(new_board)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        print(f"Integrity Error details: {error_message}")
        raise HTTPException(
            status_code=400,
            detail="A constraint was violated while attempting to create the board",
        )

    return new_board
