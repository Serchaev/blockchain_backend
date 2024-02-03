from typing import Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

from app.api_v1.schemas import BlockchainSchemaBody
from app.core import Blockchain


class BlockchainService:
    @staticmethod
    async def find_all(
        session: AsyncSession,
        limit: int,
        offset: int,
    ) -> list[Blockchain]:
        stmt = select(Blockchain).order_by(Blockchain.id).limit(limit).offset(offset)
        result: Result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def find_all_count(session: AsyncSession) -> list[Blockchain]:
        stmt = select(func.count(Blockchain.id))
        result: Result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def find(
        session: AsyncSession,
        segment_id: str,
    ) -> Optional[Blockchain]:
        stmt = select(Blockchain).where(Blockchain.segment_id == segment_id)
        result: Result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def find_by_id(
        session: AsyncSession,
        id: int,
    ) -> Optional[Blockchain]:
        stmt = select(Blockchain).where(Blockchain.id == id)
        result: Result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        session: AsyncSession,
        blockchain_data: BlockchainSchemaBody,
    ) -> Blockchain:
        blockchain = Blockchain(**blockchain_data.model_dump(exclude_none=True))
        session.add(blockchain)
        await session.commit()
        return blockchain
