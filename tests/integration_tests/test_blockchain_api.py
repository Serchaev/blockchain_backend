import pytest


class TestBlockchainGet:
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
    async def test_blockchain_api_get_blockchain(
        self,
        ac,
        segment_id,
        title,
        descr,
        deleted,
    ):
        for _ in range(2):
            response = await ac.get(f"/api/v1/blockchain/{segment_id}")

            assert response.status_code == 200

            body = response.json()

            assert body["segment_id"] == segment_id
            assert body["title"] == title
            assert body["descr"] == descr
            assert body["deleted"] == deleted

    @pytest.mark.parametrize(
        "is_pagination, limit, offset, status,",
        [
            (False, None, None, 200),
            (True, None, None, 200),
            (True, -1, -1, 422),
            (True, -1, 5, 422),
            (True, 5, -1, 422),
            (True, 10, 0, 200),
            (True, 50, 0, 200),
            (True, 15, 10, 200),
        ],
    )
    async def test_blockchain_api_get_blockchains(
        self,
        ac,
        is_pagination,
        limit,
        offset,
        status,
    ):
        if not is_pagination:
            response = await ac.get(
                "/api/v1/blockchain",
            )
        else:
            response = await ac.get(
                "/api/v1/blockchain",
                params={
                    "limit": limit,
                    "offset": offset,
                },
            )
        assert response.status_code == status

        if limit is not None and offset is not None:
            body = response.json()

            assert len(body) <= limit


class TestBlockchainPost:
    @pytest.mark.parametrize(
        "segment_id, title, descr, deleted, status,",
        [
            ("we6qgf5dh0j", None, None, False, 409),
            ("lhj5khg46mgn", "Общий", None, None, 409),
            ("4tgu95ug5gh429h", None, None, False, 201),
            ("", None, None, None, 201),
            ("e8hw45u1bf7", None, None, None, 201),
            (123456, None, None, None, 422),
        ],
    )
    async def test_blockchain_api_add_blockchain(
        self,
        ac,
        segment_id,
        title,
        descr,
        deleted,
        status,
    ):
        # assert 1 == 1
        response = await ac.post(
            "/api/v1/blockchain",
            json={
                "segment_id": segment_id,
                "title": title,
                "descr": descr,
                "deleted": deleted,
            },
        )
        #
        assert response.status_code == status

        if response.status_code == 201:
            blocks = await ac.get("/api/v1/block", params={"segment_id": segment_id})

            assert blocks.status_code == 200

            blocks_data: dict = blocks.json()

            genesis_block = blocks_data["blocks"][0]

            data = genesis_block.get("data")

            assert data

            assert data.get("Genesis") == "Block"
