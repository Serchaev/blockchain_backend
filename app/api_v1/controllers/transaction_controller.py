import json
import time
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api_v1.controllers import BlockController
from app.api_v1.schemas import TransactionSchema
from app.api_v1.services import BlockchainService
from app.core import redis_engine as r, settings


class TransactionController:
    @staticmethod
    async def add_transaction(
        session: AsyncSession,
        segment_id: str,
        transaction_data: TransactionSchema,
    ):
        segment = await BlockchainService.find(session=session, segment_id=segment_id)
        if segment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blockchain segment {segment_id} not found!",
            )
        transaction = transaction_data.model_dump()
        transaction["timestamp"] = datetime.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S%z",
        )
        await r.rpush(
            f"{settings.REDIS_PREFIX}-transaction::{segment_id}",
            json.dumps(transaction),
        )
        return transaction

    @staticmethod
    async def register_transaction(session: AsyncSession, segment_id: str):
        transactions = await r.lrange(
            f"{settings.REDIS_PREFIX}-transaction::{segment_id}",
            0,
            await r.llen(f"{settings.REDIS_PREFIX}-transaction::{segment_id}"),
        )
        transactions = [json.loads(x) for x in transactions]

        new_block = await BlockController.add_block(
            session=session,
            segment_id=segment_id,
            data=transactions,
        )
        await r.delete(f"{settings.REDIS_PREFIX}-transaction::{segment_id}")
        return new_block
