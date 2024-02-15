from fastapi import APIRouter

from app.api_v1.routers import block_router, blockchain_router, transaction_router

router = APIRouter()

router.include_router(blockchain_router)
router.include_router(transaction_router)
router.include_router(block_router)
