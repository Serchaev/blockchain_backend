import pytest

from app.api_v1.services import BlockService


class TestBlocksFind:
    @pytest.mark.parametrize(
        "id, segment_id, previous_hash, actual_hash, data,",
        [
            (1, "we6qgf5dh0j", None, None, {"Genesis": "Block"}),
            (
                2,
                "we6qgf5dh0j",
                None,
                None,
                [
                    {
                        "writer": "German",
                        "reader": "Ivan",
                        "message": "hello",
                        "timestamp": 0.0,
                    },
                    {
                        "writer": "Ivan",
                        "reader": "German",
                        "message": "hi",
                        "timestamp": 1.3456,
                    },
                ],
            ),
            (
                3,
                "we6qgf5dh0j",
                None,
                None,
                [
                    {
                        "writer": "German",
                        "reader": "Ivan",
                        "message": "how are you?",
                        "timestamp": 2.56,
                    }
                ],
            ),
            (4, "lhj5khg46mgn", None, None, {"Genesis": "Block"}),
            (5, "4tgg9uh42g5u9h", None, None, {"Genesis": "Block"}),
        ],
    )
    async def test_blocks_find(
        self,
        session,
        id,
        segment_id,
        previous_hash,
        actual_hash,
        data,
    ):
        response = await BlockService.find(
            session,
            id,
        )

        assert response.id == id
        assert response.segment_id == segment_id
        assert response.previous_hash == previous_hash
        assert response.actual_hash == actual_hash
        assert response.data == data

    async def test_blocks_find_all(self, session):
        response = await BlockService.find_all(session)

        assert isinstance(response, list)


class TestBlocksCreate:
    @pytest.mark.parametrize(
        "segment_id, previous_hash, actual_hash, data,",
        [
            ("2e8hw45ubf72", None, None, {}),
            (
                "2sz9k7kdxcfjerytih2",
                "",
                "",
                [
                    {
                        "writer": "German",
                        "reader": "Ivan",
                        "message": "how are you?",
                        "timestamp": 2.56,
                    }
                ],
            ),
            ("2lhj5khg46mgn2", "test", "test", {}),
            ("e8hw45ubf7", None, None, None),
        ],
    )
    async def test_blocks_create_success(
        self,
        session,
        segment_id,
        previous_hash,
        actual_hash,
        data,
    ):
        new_block = {
            "segment_id": segment_id,
            "previous_hash": previous_hash,
            "actual_hash": actual_hash,
        }
        if data:
            new_block["data"] = data
        response = await BlockService.create(
            session,
            **new_block,
        )

        assert response.segment_id == new_block.get("segment_id")
        assert response.previous_hash == new_block.get("previous_hash")
        assert response.actual_hash == new_block.get("actual_hash")
        if data:
            assert response.data == new_block.get("data")
        else:
            assert response.data == {}

    @pytest.mark.parametrize(
        "segment_id, previous_hash, actual_hash, data, error,",
        [
            ("1234", "", "", "", pytest.raises(Exception)),
            ("True", 345, "test", True, pytest.raises(Exception)),
        ],
    )
    async def test_blockchain_create_error(
        self,
        session,
        segment_id,
        previous_hash,
        actual_hash,
        data,
        error,
    ):
        new_block = {
            "segment_id": segment_id,
            "previous_hash": previous_hash,
            "actual_hash": actual_hash,
            "data": data,
        }
        with error:
            assert await BlockService.create(
                session,
                **new_block,
            )
