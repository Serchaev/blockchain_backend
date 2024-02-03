import time

from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
        **kwargs,
    ) -> Block:
        block = Block(**kwargs)
        session.add(block)
        await session.commit()
        return block

    @staticmethod
    async def create_genesis_block(
        session: AsyncSession,
        blockchain_id: int,
    ) -> Block:
        block = Block(
            timestamp=time.time(),
            data=str(
                [
                    {
                        "writer": "",
                        "reader": "",
                        "message": "Genesis Block",
                        "file": None,
                        "timestamp": f"{time.time()}",
                    }
                ]
            ),
            previous_hash="0",
            blockchain_id=blockchain_id,
        )
        session.add(block)
        await session.commit()
        return block
