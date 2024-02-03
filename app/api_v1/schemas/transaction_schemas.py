from typing import Optional

from pydantic import BaseModel


class TransactionSchema(BaseModel):
    data: str
