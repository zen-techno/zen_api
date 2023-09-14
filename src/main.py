from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import router
from src.database import check_database_connection


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await check_database_connection()
    yield


app = FastAPI(
    title="Zen",
    summary="REST API сервис для управления личными финансами",
    lifespan=lifespan,
)

app.include_router(router)

# TODO: Настроить логирование, Sentry
