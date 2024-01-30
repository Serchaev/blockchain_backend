from fastapi import APIRouter
from app.api_v1.routers import blockchain_router


router = APIRouter(prefix="/api/v1")

router.include_router(blockchain_router)
