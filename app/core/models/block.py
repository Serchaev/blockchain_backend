from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Block(Base):
    __tablename__ = "blocks"

    timestamp: Mapped[float]
    data: Mapped[str]
    previous_hash: Mapped[str] = mapped_column(nullable=True)
    actual_hash: Mapped[str] = mapped_column(nullable=True)
    blockchain_id: Mapped[str] = mapped_column(
        ForeignKey("blockchain.id"),
    )
