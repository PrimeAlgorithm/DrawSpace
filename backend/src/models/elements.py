import uuid
import enum
from datetime import datetime
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy import ForeignKey, DateTime, func, Enum
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from backend.src.models.boards import Board
    from backend.src.models.users import User


class ElementKind(str, enum.Enum):
    rectangle = "rectangle"
    circle = "circle"
    line = "line"
    arrow = "arrow"
    text = "text"


class Element(Base):
    __tablename__ = "elements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    board_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_created_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    kind: Mapped[ElementKind] = mapped_column(
        Enum(ElementKind, name="element_kind"),
        nullable=False,
    )
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
    properties: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    board: Mapped["Board"] = relationship(
        back_populates="elements", foreign_keys=[board_id]
    )
    created_by: Mapped[Optional["User"]] = relationship(
        back_populates="created_elements", foreign_keys=[user_created_id]
    )
