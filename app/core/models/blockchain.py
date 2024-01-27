from typing import TYPE_CHECKING, Optional

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .block import Block


class Blockchain(Base):
    __tablename__ = "blockchain"

    segment_id: Mapped[str] = mapped_column(unique=True)
    title: Mapped[Optional[str]]
    descr: Mapped[Optional[str]]
    deleted: Mapped[Optional[bool]]

    blocks: Mapped[list["Block"]] = relationship(back_populates="blockchain")
