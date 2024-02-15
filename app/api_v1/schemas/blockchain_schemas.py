from typing import Annotated, Optional

from pydantic import BaseModel, Field


class BlockchainSchema(BaseModel):
    segment_id: str
    title: Optional[str]
    descr: Optional[str]
    deleted: Optional[bool]


class BlockchainSchemaBody(BlockchainSchema):
    pass


class BlockchainSchemaAnswer(BlockchainSchema):
    pass


class BlockchainSchemaAnswerPagination(BaseModel):
    blockchain: list[BlockchainSchemaAnswer]
    count: int


class BlockchainSchemaQueryPagination:
    def __init__(
        self,
        limit: Annotated[int, Field(ge=0)] = None,
        offset: Annotated[int, Field(ge=0)] = None,
    ):
        self.limit = limit
        self.offset = offset
