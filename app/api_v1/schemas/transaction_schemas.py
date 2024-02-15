from typing import Optional

from pydantic import BaseModel


class TransactionSchema(BaseModel):
    writer: str
    reader: str
    message: str
