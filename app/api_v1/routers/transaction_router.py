from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.controllers import TransactionController
from app.api_v1.schemas import BlockSchemaAnswer, TransactionSchema
from app.core import db_factory

router = APIRouter(
    prefix="/transaction",
    tags=["транзакции"],
)


@router.post("/add/{segment_id}")
async def add_transaction(
    segment_id: str,
    transaction_data: TransactionSchema,
    session: AsyncSession = Depends(db_factory.session_depends),
):
    return await TransactionController.add_transaction(
        session=session,
        segment_id=segment_id,
        transaction_data=transaction_data,
    )


@router.post("/register/{segment_id}")
async def register_transaction(
    segment_id: str,
    session: AsyncSession = Depends(db_factory.session_depends),
) -> BlockSchemaAnswer:
    return await TransactionController.register_transaction(
        session=session,
        segment_id=segment_id,
    )
