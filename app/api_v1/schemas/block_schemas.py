from typing import Optional

from pydantic import BaseModel


class BlockSchema(BaseModel):
    blockchain_id: int
    timestamp: Optional[float]
    data: list[dict]


class BlockSchemaBody(BlockSchema):
    pass


class BlockSchemaAnswer(BlockSchema):
    id: int
    previous_hash: Optional[str]
    actual_hash: Optional[str]


class BlockSchemaAnswerPagination(BaseModel):
    blockchain: list[BlockSchemaAnswer]
    count: int


class BlockSchemaQueryPagination:
    def __init__(
        self,
        limit: int = 100,
        offset: int = 0,
    ):
        self.limit = limit
        self.offset = offset
