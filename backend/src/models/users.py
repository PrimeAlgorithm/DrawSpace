import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.core.config import (
    MAX_EMAIL_LENGTH,
    PASSWORD_HASH_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.src.models.boards import Board
    from backend.src.models.elements import Element


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(MAX_EMAIL_LENGTH), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(
        String(PASSWORD_HASH_LENGTH), nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(MAX_FIRST_NAME_LENGTH), nullable=False
    )
    last_name: Mapped[str] = mapped_column(String(MAX_LAST_NAME_LENGTH), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    boards: Mapped[list["Board"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    created_elements: Mapped[list["Element"]] = relationship(
        back_populates="created_by",
        foreign_keys="Element.user_created_id",
        passive_deletes=True,
    )
