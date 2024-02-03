from app.api_v1.schemas import TransactionSchema


class TransactionController:
    @staticmethod
    async def add_transaction(segment_id: str, transaction_data: TransactionSchema):
        pass

    @staticmethod
    async def register_transaction(segment_id: str):
        pass
