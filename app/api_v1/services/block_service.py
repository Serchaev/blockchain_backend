from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core import Block, Blockchain


class BlockService:
    @staticmethod
    async def find_all(
        session: AsyncSession,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        segment_id: Optional[str] = None,
    ) -> list[Block]:
        stmt = (
            select(Block)
            .join(Block.blockchain)
            .order_by(Block.id)
            .options(joinedload(Block.blockchain))
        )
        if limit is not None:
            stmt = stmt.limit(limit=limit)
        if offset is not None:
            stmt = stmt.offset(offset=offset)
        if segment_id is not None:
            stmt = stmt.where(Blockchain.segment_id == segment_id)
        result: Result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def find_all_count(
        session: AsyncSession,
        segment_id: str = None,
    ) -> int:
        stmt = select(func.count(Block.id))
        if segment_id is not None:
            stmt = stmt.join(Block.blockchain).where(
                Blockchain.segment_id == segment_id
            )
        result: Result = await session.execute(stmt)
        return result.scalar()

    @staticmethod
    async def find(
        session: AsyncSession,
        id: int,
    ) -> Block:
        stmt = select(Block).where(Block.id == id).options(joinedload(Block.blockchain))
        result: Result = await session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    async def create(
        session: AsyncSession,
        **kwargs,
    ) -> Block:
        block = Block(**kwargs)
        session.add(block)
        await session.commit()
        return block

    @staticmethod
    async def create_genesis_block(
        session: AsyncSession,
        segment_id: str,
    ) -> Block:
        block = Block(
            data={"Genesis": "Block"},
            previous_hash="0",
            segment_id=segment_id,
        )
        session.add(block)
        await session.commit()
        return block
