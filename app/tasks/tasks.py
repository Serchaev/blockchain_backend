import multiprocessing
from typing import Optional

from pysecurechain import Block as _Block
from sqlalchemy import desc, select, update

from app.core import Block, Blockchain, db_factory
from app.tasks.config import celery_app


def get_blockchain(session):
    result = session.execute(select(Blockchain))
    return result.scalars().all()


def get_last_block_is_not_none(session, element):
    stmt = (
        select(Block)
        .where(Block.segment_id == element.segment_id)
        .filter(Block.actual_hash.isnot(None))
        .order_by(desc(Block.id))
        .limit(1)
    )
    result = session.execute(stmt)
    block: Optional[Block] = result.scalar_one_or_none()
    return block


def get_last_block_is_none(session, element):
    stmt = (
        select(Block)
        .where(Block.segment_id == element.segment_id)
        .filter(Block.actual_hash.is_(None))
        .order_by(Block.id)
    )
    result = session.execute(stmt)
    blocks: list[Block] = result.scalars().all()
    return blocks


def get_segment(session, element):
    segment = []
    last_block = get_last_block_is_not_none(session, element)
    if last_block is not None:
        segment.append(last_block)
    new_blocks = get_last_block_is_none(session, element)
    segment.extend(new_blocks)
    return segment


def py_secure_chain(block: Block):
    new_block = _Block(
        id=block.id,
        segment_id=block.segment_id,
        timestamp=block.created_at,
        data=block.data,
        previous_hash=block.previous_hash,
    )
    return new_block


def run_proccess_calculate(segment_id: int, segment: list[Block]):
    new_segment = []
    previous_hash = "0"
    for elem in segment:
        if elem.previous_hash is None:
            elem.previous_hash = previous_hash
        new_block = py_secure_chain(elem)
        previous_hash = new_block.actual_hash
        new_segment.append(new_block)
    return segment_id, new_segment


@celery_app.task
def calculate_hash():
    with db_factory.sync_session_factory() as session:
        blockchain = get_blockchain(session)

        segments = {}
        for element in blockchain:
            segment = get_segment(session, element)
            if len(segment) >= 2:
                segments[element.segment_id] = get_segment(session, element)

        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        results = []
        for index, value in segments.items():
            result = pool.apply_async(
                run_proccess_calculate,
                (
                    index,
                    value,
                ),
            )
            results.append(result)

        pool.close()
        pool.join()

        for result in results:
            segment_id, segment_list = result.get()
            for element in segment_list:
                stmt = (
                    update(Block)
                    .where(Block.id == element.id)
                    .values(
                        previous_hash=element.previous_hash,
                        actual_hash=element.actual_hash,
                    )
                )
                session.execute(stmt)

        session.commit()
