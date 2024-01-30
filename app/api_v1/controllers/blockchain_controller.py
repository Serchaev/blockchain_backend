from typing import Optional

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.dependencies import BlockchainFindDepends
from app.api_v1.schemas import BlockchainSchemaBody
from app.api_v1.services import BlockchainService
from app.core import Blockchain


class BlockchainController:
    @staticmethod
    async def get_blockchains(
        session: AsyncSession,
        limit: int,
        offset: int,
    ) -> list[Blockchain]:
        segments = await BlockchainService.find_all(
            session=session,
            limit=limit,
            offset=offset,
        )
        segments_count = await BlockchainService.find_all_count(
            session=session,
        )
        answer = {"blockchain": segments, "count": segments_count}
        return answer

    @staticmethod
    async def get_blockchain(session: AsyncSession, segment_id: str):
        segment = await BlockchainService.find(session=session, segment_id=segment_id)
        if segment is not None:
            return segment

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blockchain segment {segment_id} not found!",
        )

    @staticmethod
    async def add_blockchain(
        session: AsyncSession,
        blockchain_data: BlockchainSchemaBody,
    ) -> Blockchain:
        segment = await BlockchainService.find(
            session=session,
            segment_id=blockchain_data.segment_id,
        )
        if segment is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Blockchain segment {blockchain_data.segment_id} already exists!",
            )
        return await BlockchainService.create(
            session=session,
            blockchain_data=blockchain_data,
        )
