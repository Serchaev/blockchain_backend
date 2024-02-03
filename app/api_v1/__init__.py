from fastapi import APIRouter
from app.api_v1.routers import blockchain_router, block_router, transaction_router

router = APIRouter(prefix="/api/v1")

router.include_router(blockchain_router)
router.include_router(transaction_router)
router.include_router(block_router)
