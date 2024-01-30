import uvicorn
from fastapi import FastAPI
from app.api_v1 import router

app = FastAPI()

app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=25565)
