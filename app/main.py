from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.api_v1 import router
from app.core import settings


@asynccontextmanager
async def lifespan(server: FastAPI):
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix=settings.REDIS_PREFIX)
    yield


app = FastAPI(lifespan=lifespan)

app_v1 = FastAPI(
    title="API v1",
    description="The first version of API",
    docs_url="/docs",
    redoc_url="/redoc",
    version="1.0",
)

app_v1.include_router(router=router)

app.mount("/api/v1", app_v1)


@app.get("/api")
async def api():
    return {"url": "/api/v1/docs"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
