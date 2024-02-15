import asyncio
import json
from typing import Union, Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.services import BlockchainService, BlockService
from app.core import Block


class BlockController:
    @staticmethod
    async def get_blocks(
        session: AsyncSession,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        segment_id: str = None,
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
        answer = {"blocks": blocks, "count": blocks_count}
        return answer

    @staticmethod
    async def get_block(
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
        segment_id: str,
        **kwargs,
    ) -> Block:
        blockchain = await BlockchainService.find(
            session=session,
            segment_id=segment_id,
        )
        if blockchain is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blockchain {kwargs.get('blockchain_id')} not found!",
            )
        block = await BlockService.create(
            session=session,
            segment_id=blockchain.segment_id,
            **kwargs,
        )
        block.blockchain = blockchain
        return block
