from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

if TYPE_CHECKING:
    from .blockchain import Blockchain


class Block(Base):
    __tablename__ = "blocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    previous_hash: Mapped[str] = mapped_column(nullable=True)
    actual_hash: Mapped[str] = mapped_column(nullable=True)
    segment_id: Mapped[str] = mapped_column(
        ForeignKey("blockchain.segment_id"),
    )
    data = Column(
        JSONB,
        default=text("'{}'::jsonb"),
        server_default=text("'{}'::jsonb"),
    )
    blockchain: Mapped["Blockchain"] = relationship(back_populates="blocks")

    def __str__(self):
        return f'{self.__class__.__name__}(segment_id={self.segment_id}, data="{self.data}", previous_hash="{self.previous_hash}", actual_hash="{self.actual_hash}", timestamp={self.timestamp})'

    def __repr__(self):
        return self.__str__()
