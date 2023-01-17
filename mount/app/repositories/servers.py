from typing import Any

from app.common.context import Context
from app.models import Status

READ_PARAMS = """\
    server_id, server_name, hourly_request_limit, status, created_at, updated_at
"""


async def create(
    ctx: Context,
    server_name: str,
    hourly_request_limit: int,
    secret_key: str,
    status: Status = Status.ACTIVE,
) -> dict[str, Any]:
    query = f"""\
        INSERT INTO servers (server_name, hourly_request_limit, secret_key,
                             status)
             VALUES (:server_name, :hourly_request_limit, :secret_key,
                     :status)
    """
    params: dict[str, Any] = {
        "server_name": server_name,
        "hourly_request_limit": hourly_request_limit,
        "secret_key": secret_key,
        "status": status,
    }
    rec_id = await ctx.db.execute(query, params)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM servers
         WHERE server_id = :server_id
    """
    params: dict[str, Any] = {
        "server_id": rec_id,
    }
    rec = await ctx.db.fetch_one(query, params)
    assert rec is not None
    return dict(rec)


async def fetch_one(
    ctx: Context,
    server_id: int | None = None,
    server_name: str | None = None,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM servers
         WHERE server_id = COALESCE(:server_id, server_id)
           AND server_name = COALESCE(:server_name, server_name)
           AND status = :status
    """
    params: dict[str, Any] = {
        "server_id": server_id,
        "server_name": server_name,
        "status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    return dict(rec) if rec is not None else None


async def fetch_many(
    ctx: Context,
    page: int | None = None,
    page_size: int | None = None,
    status: Status = Status.ACTIVE,
) -> list[dict[str, Any]]:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM servers
         WHERE status = :status
    """
    params: dict[str, Any] = {
        "status": status,
    }

    if page is not None and page_size is not None:
        query += """\
            LIMIT :limit
           OFFSET :offset
        """
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size

    recs = await ctx.db.fetch_all(query, params)
    return [dict(rec) for rec in recs]


async def partial_update(
    ctx: Context,
    server_id: int,
    server_name: str | None = None,
    hourly_request_limit: int | None = None,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        UPDATE servers
           SET server_name = COALESCE(:server_name, server_name),
               hourly_request_limit = COALESCE(:hourly_request_limit, hourly_request_limit),
               updated_at = NOW()
         WHERE server_id = :server_id
           AND status = :status
    """
    params: dict[str, Any] = {
        "server_id": server_id,
        "server_name": server_name,
        "hourly_request_limit": hourly_request_limit,
        "status": status,
    }
    await ctx.db.execute(query, params)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM servers
         WHERE server_id = :server_id
    """
    params: dict[str, Any] = {
        "server_id": server_id,
    }
    rec = await ctx.db.fetch_one(query, params)
    return dict(rec) if rec is not None else None


async def delete(
    ctx: Context,
    server_id: int,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        UPDATE servers
           SET status = :new_status,
               updated_at = NOW()
         WHERE server_id = :server_id
           AND status = :old_status
    """
    params: dict[str, Any] = {
        "server_id": server_id,
        "new_status": Status.DELETED,
        "old_status": status,
    }
    await ctx.db.execute(query, params)

    query = f"""\
        SELECT {READ_PARAMS}
          FROM servers
         WHERE server_id = :server_id
           AND status = :new_status
    """
    params: dict[str, Any] = {
        "server_id": server_id,
        "new_status": Status.DELETED,
    }
    rec = await ctx.db.fetch_one(query, params)
    return dict(rec) if rec is not None else None
