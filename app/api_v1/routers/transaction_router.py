from fastapi import APIRouter, Depends

from app.api_v1.controllers import TransactionController
from app.api_v1.schemas import TransactionSchema

router = APIRouter(
    prefix="/transaction",
    tags=["транзакции"],
)


@router.post("/add/{segment_id}")
async def add_transaction(
    segment_id: str,
    transaction_data: TransactionSchema = Depends(TransactionSchema),
):
    return await TransactionController.add_transaction(
        segment_id=segment_id,
        transaction_data=transaction_data,
    )


@router.post("/register/{segment_id}")
async def register_transaction(
    segment_id: str,
):
    return await TransactionController.register_transaction(segment_id=segment_id)
