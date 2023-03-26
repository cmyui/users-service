import traceback
from typing import Any
from uuid import uuid4

from app.common import logger
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories import servers as servers_repo


async def create(
    ctx: Context,
    server_name: str,
    hourly_request_limit: int,
) -> dict[str, Any] | ServiceError:
    if await servers_repo.fetch_one(ctx, server_name=server_name):
        return ServiceError.SERVERS_NAME_ALREADY_EXISTS

    transaction = await ctx.db.transaction()

    try:
        secret_key = str(uuid4())
        server = await servers_repo.create(
            ctx,
            server_name,
            hourly_request_limit,
            secret_key,
        )
    except Exception as exc:  # pragma: no cover
        await transaction.rollback()
        logger.error("Unable to create server:", error=exc)
        logger.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.SERVERS_CREATION_FAILED
    else:
        await transaction.commit()

    return server


async def fetch_one(
    ctx: Context,
    server_id: int | None = None,
    server_name: str | None = None,
) -> dict[str, Any] | ServiceError:
    server = await servers_repo.fetch_one(ctx, server_id, server_name)

    if server is None:
        return ServiceError.SERVERS_NOT_FOUND

    return server


async def fetch_many(
    ctx: Context,
    page: int | None = None,
    page_size: int | None = None,
) -> list[dict[str, Any]]:
    servers = await servers_repo.fetch_many(ctx, page, page_size)
    return servers


async def partial_update(
    ctx: Context,
    server_id: int,
    server_name: str | None = None,
    hourly_request_limit: int | None = None,
) -> dict[str, Any] | ServiceError:
    server = await servers_repo.partial_update(
        ctx,
        server_id,
        server_name,
        hourly_request_limit,
    )

    if server is None:
        return ServiceError.SERVERS_NOT_FOUND

    return server


async def delete(
    ctx: Context,
    server_id: int,
) -> dict[str, Any] | ServiceError:
    server = await servers_repo.delete(ctx, server_id)

    if server is None:
        return ServiceError.SERVERS_NOT_FOUND

    return server
