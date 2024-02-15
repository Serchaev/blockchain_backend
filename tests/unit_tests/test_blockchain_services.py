import pytest
from sqlalchemy.exc import DBAPIError, IntegrityError, StatementError

from app.api_v1.services import BlockchainService


class TestBlockchainFind:
    @pytest.mark.parametrize(
        "segment_id, title, descr, deleted,",
        [
            ("we6qgf5dh0j", None, None, False),
            ("lhj5khg46mgn", "Общий", None, None),
            ("4tgg9uh42g5u9h", None, None, True),
            ("sz9k7kdxcfjerytih", "Рабочая", None, False),
            ("e8hw45ubf7", None, None, None),
        ],
    )
    async def test_blockchain_find(self, session, segment_id, title, descr, deleted):
        response = await BlockchainService.find(
            session,
            segment_id,
        )

        assert response.segment_id == segment_id
        assert response.title == title
        assert response.descr == descr
        assert response.deleted == deleted

    async def test_blockchain_find_all_count(self, session):
        assert await BlockchainService.find_all_count(session) >= 12


class TestBlockchainCreate:
    @pytest.mark.parametrize(
        "segment_id, title, descr, deleted,",
        [
            ("-1", None, None, None),
            ("123", "", "", False),
            ("434thrdyy", "test", "test", True),
        ],
    )
    async def test_blockchain_create_success(
        self,
        session,
        segment_id,
        title,
        descr,
        deleted,
    ):
        new_segment = {
            "segment_id": segment_id,
            "title": title,
            "descr": descr,
            "deleted": deleted,
        }
        response = await BlockchainService.create(
            session,
            **new_segment,
        )

        assert response.segment_id == new_segment.get("segment_id")
        assert response.title == new_segment.get("title")
        assert response.descr == new_segment.get("descr")
        assert response.deleted == new_segment.get("deleted")

    @pytest.mark.parametrize(
        "segment_id, title, descr, deleted, error,",
        [
            ("e8hw45ubf7", None, None, None, pytest.raises(IntegrityError)),
            ("1234", "", "", "", pytest.raises(StatementError)),
            ("True", 345, "test", True, pytest.raises(DBAPIError)),
        ],
    )
    async def test_blockchain_create_error(
        self,
        session,
        segment_id,
        title,
        descr,
        deleted,
        error,
    ):
        new_segment = {
            "segment_id": segment_id,
            "title": title,
            "descr": descr,
            "deleted": deleted,
        }
        with error:
            assert await BlockchainService.create(
                session,
                **new_segment,
            )
