import pytest


class TestBlocksGet:
    @pytest.mark.parametrize(
        "id, segment_id, previous_hash, actual_hash, data, title, descr, deleted,",
        [
            (1, "we6qgf5dh0j", "0", None, {"Genesis": "Block"}, None, None, False),
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
                None,
                None,
                False,
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
                None,
                None,
                False,
            ),
            (4, "lhj5khg46mgn", "0", None, {"Genesis": "Block"}, "Общий", None, None),
            (5, "4tgg9uh42g5u9h", "0", None, {"Genesis": "Block"}, None, None, True),
        ],
    )
    async def test_block_api_get_block(
        self,
        ac,
        id,
        segment_id,
        previous_hash,
        actual_hash,
        data,
        title,
        descr,
        deleted,
    ):
        for _ in range(2):
            response = await ac.get(f"/api/v1/block/{id}")

            assert response.status_code == 200

            body = response.json()

            assert body["id"] == id
            assert body["segment_id"] == segment_id
            assert body["previous_hash"] == previous_hash
            assert body["actual_hash"] == actual_hash
            assert body["data"] == data
            assert body["blockchain"]["title"] == title
            assert body["blockchain"]["descr"] == descr
            assert body["blockchain"]["deleted"] == deleted

    @pytest.mark.parametrize(
        "is_pagination, limit, offset, status,",
        [
            (False, None, None, 200),
            (True, None, None, 422),
            (True, -1, -1, 422),
            (True, -1, 5, 422),
            (True, 5, -1, 422),
            (True, 10, 0, 200),
            (True, 50, 0, 200),
            (True, 15, 10, 200),
        ],
    )
    async def test_block_api_get_blocks(
        self,
        ac,
        is_pagination,
        limit,
        offset,
        status,
    ):
        if not is_pagination:
            response = await ac.get(
                "/api/v1/block",
            )
        else:
            response = await ac.get(
                "/api/v1/block",
                params={
                    "limit": limit,
                    "offset": offset,
                },
            )
        assert response.status_code == status

        if limit is not None and offset is not None and limit >= 0 and offset >= 0:
            body = response.json()

            assert len(body) <= limit
