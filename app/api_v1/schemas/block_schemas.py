from typing import Optional

from pydantic import BaseModel


class BlockSchema(BaseModel):
    blockchain_id: int
    timestamp: Optional[float]
    data: str


class _BlockchainSchema(BaseModel):
    id: int
    segment_id: str
    title: Optional[str]
    descr: Optional[str]
    deleted: Optional[bool]


class BlockSchemaAnswer(BlockSchema):
    id: int
    previous_hash: Optional[str]
    actual_hash: Optional[str]
    blockchain: _BlockchainSchema


class BlockSchemaAnswerPagination(BaseModel):
    blocks: list[BlockSchemaAnswer]
    count: int


class BlockSchemaQueryPagination:
    def __init__(
        self,
        limit: int = 100,
        offset: int = 0,
    ):
        self.limit = limit
        self.offset = offset


class BlockSchemaQuery:
    def __init__(
        self,
        segment_id: str = None,
    ):
        self.segment_id = segment_id
