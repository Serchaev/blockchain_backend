from typing import Optional

from pydantic import BaseModel


class BlockchainSchema(BaseModel):
    segment_id: str
    title: Optional[str]
    descr: Optional[str]
    deleted: Optional[bool]


class BlockchainSchemaBody(BlockchainSchema):
    pass


class BlockchainSchemaAnswer(BlockchainSchema):
    id: int


class BlockchainSchemaAnswerPagination(BaseModel):
    blockchain: list[BlockchainSchemaAnswer]
    count: int


class BlockchainSchemaQueryPagination:
    def __init__(
        self,
        limit: int = 10,
        offset: int = 0,
    ):
        self.limit = limit
        self.offset = offset
