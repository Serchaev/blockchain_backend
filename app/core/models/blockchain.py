from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class Blockchain(Base):
    __tablename__ = "blockchain"

    segment_id: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]
    descr: Mapped[str]
    deleted: Mapped[bool]
