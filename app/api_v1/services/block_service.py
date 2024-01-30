from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api_v1.schemas import BlockSchemaBody
from app.core import Block, Blockchain


class BlockService:
    @staticmethod
    async def find_all(
        session: AsyncSession,
        segment_id: str = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Block]:
        stmt = (
            select(Block)
            .join(Block.blockchain)
            .order_by(Block.id)
            .limit(limit=limit)
            .offset(offset=offset)
            .options(joinedload(Block.blockchain))
        )
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
        block_data: BlockSchemaBody,
    ) -> Block:
        block = Block(**block_data.model_dump(exclude_none=True))
        session.add(block)
        await session.commit()
        return block
