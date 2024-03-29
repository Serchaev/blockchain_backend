from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.controllers import BlockchainController
from app.api_v1.schemas import (
    BlockchainSchemaAnswer,
    BlockchainSchemaAnswerPagination,
    BlockchainSchemaBody,
    BlockchainSchemaQueryPagination,
)
from app.core import db_factory

router = APIRouter(
    tags=["Блокчейн"],
    prefix="/blockchain",
)


@router.get("", status_code=status.HTTP_200_OK)
@cache(expire=60)
async def get_blockchains(
    pagination: BlockchainSchemaQueryPagination = Depends(
        BlockchainSchemaQueryPagination
    ),
    session: AsyncSession = Depends(db_factory.session_depends),
) -> BlockchainSchemaAnswerPagination:
    return await BlockchainController.get_blockchains(
        session=session,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/{segment_id}", status_code=status.HTTP_200_OK)
@cache(expire=10)
async def get_blockchain(
    segment_id: str,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> BlockchainSchemaAnswer:
    return await BlockchainController.get_blockchain(
        session=session,
        segment_id=segment_id,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)  # создает новый сегмент с genesis блоком
async def add_blockchain(
    blockchain_data: BlockchainSchemaBody,
    session: AsyncSession = Depends(
        db_factory.session_depends,
    ),
):
    return await BlockchainController.add_blockchain(
        session=session,
        blockchain_data=blockchain_data,
    )
