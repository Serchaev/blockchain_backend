from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .block import Block


class Blockchain(Base):
    __tablename__ = "blockchain"

    segment_id: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    descr: Mapped[str]
    deleted: Mapped[bool]

    blocks: Mapped[list["Block"]] = relationship(back_populates="blockchain")
