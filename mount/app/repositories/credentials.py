from typing import Any
from uuid import UUID

from app.common.context import Context
from app.models import Status

READ_PARAMS = """\
    credentials_id, account_id, identifier, secret,
    status, created_at, updated_at
"""


async def create(
    ctx: Context,
    credentials_id: UUID,
    account_id: UUID,
    identifier: str,
    secret: str,
    status: Status = Status.ACTIVE,
) -> dict[str, Any]:
    query = f"""\
        INSERT INTO credentials (credentials_id, account_id, identifier,
                                 secret, status, created_at, updated_at)
             VALUES (:credentials_id, :account_id, :identifier,
                     :secret, :status, NOW(), NOW())
          RETURNING {READ_PARAMS}
    """
    params: dict[str, Any] = {
        "credentials_id": credentials_id,
        "account_id": account_id,
        "identifier": identifier,
        "secret": secret,
        "status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    assert rec is not None
    return rec


async def fetch_one(
    ctx: Context,
    credentials_id: UUID | None = None,
    identifier: str | None = None,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM credentials
         WHERE credentials_id = COALESCE(:credentials_id, credentials_id)
           AND identifier = COALESCE(:identifier, identifier)
           AND status = :status
    """
    params: dict[str, Any] = {
        "credentials_id": credentials_id,
        "identifier": identifier,
        "status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    return rec


async def fetch_many(
    ctx: Context,
    account_id: UUID | None = None,
    page: int | None = None,
    page_size: int | None = None,
    status: Status = Status.ACTIVE,
) -> list[dict[str, Any]]:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM credentials
         WHERE account_id = COALESCE(:account_id, account_id)
           AND status = :status
    """
    params: dict[str, Any] = {
        "account_id": account_id,
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
    return recs


# credentials_id, account_id, identifier, secret,
# status, created_at, updated_at


async def partial_update(
    ctx: Context,
    credentials_id: UUID,
    identifier: str | None = None,
    secret: str | None = None,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        UPDATE credentials
           SET identifier = COALESCE(:identifier, identifier),
               secret = COALESCE(:secret, secret),
               updated_at = NOW()
         WHERE credentials_id = :credentials_id
           AND status = :status
     RETURNING {READ_PARAMS}
    """
    params: dict[str, Any] = {
        "credentials_id": credentials_id,
        "identifier": identifier,
        "secret": secret,
        "status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    return rec


async def delete(
    ctx: Context,
    credentials_id: UUID,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        UPDATE credentials
           SET status = :new_status,
               updated_at = NOW()
         WHERE credentials_id = :credentials_id
           AND status = :old_status
     RETURNING {READ_PARAMS}
    """
    params: dict[str, Any] = {
        "credentials_id": credentials_id,
        "new_status": Status.DELETED,
        "old_status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    return rec
