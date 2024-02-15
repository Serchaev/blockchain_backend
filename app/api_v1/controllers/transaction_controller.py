import time

from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.controllers import BlockController
from app.api_v1.schemas import TransactionSchema
from app.core import redis_engine as r


class TransactionController:
    @staticmethod
    async def add_transaction(segment_id: str, transaction_data: TransactionSchema):
        r.rpush(f"blockchain_transaction::{segment_id}", transaction_data.data)

    @staticmethod
    async def register_transaction(session: AsyncSession, segment_id: str):
        transactions = [
            r.lindex(
                name=f"blockchain_transaction::{segment_id}",
                index=index,
            )
            for index in range(
                r.llen(
                    name=f"blockchain_transaction::{segment_id}",
                )
            )
        ]

        r.delete(f"blockchain_transaction::{segment_id}")

        return await BlockController.add_block(
            session=session,
            segment_id=segment_id,
            timestamp=time.time(),
            data=str(transactions),
        )
