import asyncio
import json
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.services import BlockService, BlockchainService
from app.core import Block


class BlockController:
    @staticmethod
    async def get_blocks(
        session: AsyncSession,
        segment_id: str = None,
        limit: int = 100,
        offset: int = 0,
    ) -> dict[str, Union[list[Block], int]]:
        blocks = await BlockService.find_all(
            session=session,
            segment_id=segment_id,
            limit=limit,
            offset=offset,
        )
        blocks_count = await BlockService.find_all_count(
            session=session,
            segment_id=segment_id,
        )
        for block in blocks:
            block.data = json.loads(block.data)
        # await asyncio.sleep(5)
        answer = {"blocks": blocks, "count": blocks_count}
        return answer

    @staticmethod
    async def get_Block(
        session: AsyncSession,
        id: int,
    ) -> Block:
        block = await BlockService.find(
            session=session,
            id=id,
        )
        if block is not None:
            return block

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block {id} not found!",
        )

    @staticmethod
    async def add_block(
        session: AsyncSession,
        **kwargs,
    ) -> Block:
        blockchain = await BlockchainService.find_by_id(
            session=session,
            id=kwargs.get("blockchain_id"),
        )
        if blockchain is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blockchain {kwargs.get('blockchain_id')} not found!",
            )
        kwargs["data"] = str(kwargs.get("data"))
        block = await BlockService.create(
            session=session,
            **kwargs,
        )
        block.blockchain = blockchain
        return block
