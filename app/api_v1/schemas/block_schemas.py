from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field


class BlockSchema(BaseModel):
    segment_id: str
    data: Union[dict, list[dict]]


class _BlockchainSchema(BaseModel):
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
        limit: Annotated[int, Field(ge=0)] = None,
        offset: Annotated[int, Field(ge=0)] = None,
    ):
        self.limit = limit
        self.offset = offset


class BlockSchemaQuery:
    def __init__(
        self,
        segment_id: str = None,
    ):
        self.segment_id = segment_id
