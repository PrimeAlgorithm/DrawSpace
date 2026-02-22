from typing import List, Optional
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.models.elements import ElementKind
from src.database import get_db
from src.models.boards import Board
from src.models.users import User
from src.core import security


router = APIRouter()


class BoardIn(BaseModel):
    name: str


class ElementsOut(BaseModel):
    id: UUID
    board_id: UUID
    user_created_id: Optional[UUID]
    kind: ElementKind
    z_index: int


class BoardHighLevelOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BoardDetailsOut(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    elements: list[ElementsOut]

    model_config = ConfigDict(from_attributes=True)


@router.post("/", response_model=BoardHighLevelOut)
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


@router.get("/", response_model=List[BoardHighLevelOut])
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


@router.get("/{board_id}", response_model=BoardDetailsOut)
async def get_board(
    board_id: UUID,
    user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> Board:
    try:
        result = db.query(Board).filter_by(id=board_id, user_id=user.id).first()

        if not result:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Board could not be found")

        return result
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        print(f"Database error during login: {e}")
        raise HTTPException(status_code=500, detail="A database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal server error occurred")


@router.put("/{board_id}", response_model=BoardHighLevelOut)
async def update_board_name(
    board_id: UUID,
    board_in: BoardIn,
    user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> Board:
    try:
        board = db.query(Board).filter_by(id=board_id, user_id=user.id).first()

        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found",
            )

        # Make sure it's not empty
        if board_in.name != "":
            board.name = board_in.name

        db.commit()
        db.refresh(board)

        return board

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update violates database constraints",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@router.delete("/{board_id}")
async def delete_board_name(
    board_id: UUID,
    user: User = Depends(security.get_current_user),
    db: Session = Depends(get_db),
):
    try:
        board = db.query(Board).filter_by(id=board_id, user_id=user.id).first()

        if not board:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Board not found",
            )

        db.delete(board)
        db.commit()

        return None

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Update violates database constraints",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )
