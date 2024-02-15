from asyncio import current_task
from datetime import datetime

import redis
from sqlalchemy import NullPool, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from app.core.config import settings

if settings.MODE == "TEST":
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_PARAMS = {}


class DatabaseFactory:
    def __init__(
        self,
        db_url: str,
        db_echo: bool = False,
    ):
        self.engine = create_async_engine(
            url=db_url,
            echo=db_echo,
            **DATABASE_PARAMS,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_depends(self):
        async with self.session_factory() as session:
            yield session
            await session.close()


db_factory = DatabaseFactory(
    db_url=settings.db_url,
    db_echo=settings.db_echo,
)


class RedisFactory:
    def __init__(self, host, port, prefix):
        self.host = host
        self.port = port
        self.prefix = prefix
        self.r = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
        )

    def engine(self):
        return self.r


redis_factory = RedisFactory(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    prefix=settings.REDIS_PREFIX,
)

redis_engine = redis_factory.engine()


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        return f"{self.__name__.lower()}s"

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    # updated_at: Mapped[datetime] = mapped_column(
    #     default=func.now(),
    #     onupdate=func.now(),
    # )

    # id: Mapped[int] = mapped_column(primary_key=True)
