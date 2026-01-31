from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.settings import settings
from src.presentation.fastapi.routers.base import public_router, protected_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, root_path=settings.ROOT_PATH)

app.include_router(public_router)
app.include_router(protected_router)
