from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import Base, engine
from src.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"Hello": "World"}
