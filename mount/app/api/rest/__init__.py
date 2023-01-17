from __future__ import annotations

import time

from app.common import logger
from app.common import settings
from app.services import database
from fastapi import FastAPI
from fastapi import Request


def init_db(api: FastAPI) -> None:
    @api.on_event("startup")
    async def startup_db() -> None:
        logger.info("Starting up database pool")
        service_database = database.ServiceDatabase(
            read_dsn=database.dsn(
                driver=settings.WRITE_DB_DRIVER,
                user=settings.READ_DB_USER,
                password=settings.READ_DB_PASS,
                host=settings.READ_DB_HOST,
                port=settings.READ_DB_PORT,
                database=settings.READ_DB_NAME,
            ),
            write_dsn=database.dsn(
                driver=settings.WRITE_DB_DRIVER,
                user=settings.WRITE_DB_USER,
                password=settings.WRITE_DB_PASS,
                host=settings.WRITE_DB_HOST,
                port=settings.WRITE_DB_PORT,
                database=settings.WRITE_DB_NAME,
            ),
            min_pool_size=settings.MIN_DB_POOL_SIZE,
            max_pool_size=settings.MAX_DB_POOL_SIZE,
            ssl=settings.DB_USE_SSL,
        )
        await service_database.connect()
        api.state.db = service_database
        logger.info("Database pool started up")

    @api.on_event("shutdown")
    async def shutdown_db() -> None:
        logger.info("Shutting down database pool")
        await api.state.db.disconnect()
        del api.state.db
        logger.info("Database pool shut down")


def init_middlewares(api: FastAPI) -> None:
    # NOTE: these run bottom to top

    @api.middleware("http")
    async def add_db_to_request(request: Request, call_next):
        async with request.app.state.db.connection() as conn:
            request.state.db = conn
            response = await call_next(request)
        return response

    @api.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.perf_counter_ns()
        response = await call_next(request)
        process_time = (time.perf_counter_ns() - start_time) / 1e6
        response.headers["X-Process-Time"] = str(process_time)  # ms
        return response


def init_routes(api: FastAPI) -> None:
    from .v1 import router as v1_router

    api.include_router(v1_router)


def init_api():
    api = FastAPI()

    init_db(api)
    init_middlewares(api)
    init_routes(api)

    return api
