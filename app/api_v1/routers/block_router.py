from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.controllers import BlockController
from app.api_v1.schemas import (
    BlockSchemaAnswer,
    BlockSchemaAnswerPagination,
    BlockSchemaQuery,
    BlockSchemaQueryPagination,
)
from app.core import db_factory

router = APIRouter(
    prefix="/block",
    tags=["Блоки"],
)


@router.get("", status_code=status.HTTP_200_OK)
@cache(expire=10)
async def get_blocks(
    block_data: BlockSchemaQuery = Depends(BlockSchemaQuery),
    pagination: BlockSchemaQueryPagination = Depends(BlockSchemaQueryPagination),
    session: AsyncSession = Depends(db_factory.session_depends),
) -> BlockSchemaAnswerPagination:
    return await BlockController.get_blocks(
        session=session,
        segment_id=block_data.segment_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/{id}", status_code=status.HTTP_200_OK)
@cache(expire=300)
async def get_block(
    id: int,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> BlockSchemaAnswer:
    return await BlockController.get_block(
        session=session,
        id=id,
    )
