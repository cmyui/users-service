from typing import Any

from app.common.context import Context
from app.models import Status

READ_PARAMS = """\
    account_id, phone_number, first_name, last_name,
    status, created_at, updated_at
"""


async def create(
    ctx: Context,
    phone_number: str,
    hashed_password: str,
    first_name: str,
    last_name: str,
    status: Status = Status.ACTIVE,
) -> dict[str, Any]:
    query = f"""\
        INSERT INTO accounts (phone_number, hashed_password, first_name, last_name,
                              status)
             VALUES (:phone_number, :hashed_password, :first_name, :last_name,
                     :status)
          RETURNING {READ_PARAMS}
    """
    params: dict[str, Any] = {
        "phone_number": phone_number,
        "hashed_password": hashed_password,
        "first_name": first_name,
        "last_name": last_name,
        "status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    assert rec is not None
    return rec


async def fetch_one(
    ctx: Context,
    account_id: int | None = None,
    phone_number: str | None = None,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM servers
         WHERE account_id = COALESCE(:account_id, account_id)
           AND phone_number = COALESCE(:phone_number, phone_number)
           AND status = :status
    """
    params: dict[str, Any] = {
        "account_id": account_id,
        "phone_number": phone_number,
        "status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    return rec


async def fetch_many(
    ctx: Context,
    page: int | None = None,
    page_size: int | None = None,
    status: Status = Status.ACTIVE,
) -> list[dict[str, Any]]:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM accounts
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
    return recs


async def partial_update(
    ctx: Context,
    account_id: int,
    phone_number: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        UPDATE accounts
           SET phone_number = COALESCE(:phone_number, phone_number),
               first_name = COALESCE(:first_name, first_name),
               last_name = COALESCE(:last_name, last_name),
               updated_at = NOW()
         WHERE server_id = :server_id
           AND status = :status
     RETURNING {READ_PARAMS}
    """
    params: dict[str, Any] = {
        "account_id": account_id,
        "phone_number": phone_number,
        "first_name": first_name,
        "last_name": last_name,
        "status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    return rec


async def delete(
    ctx: Context,
    account_id: int,
    status: Status = Status.ACTIVE,
) -> dict[str, Any] | None:
    query = f"""\
        UPDATE accounts
           SET status = :new_status,
               updated_at = NOW()
         WHERE account_id = :account_id
           AND status = :old_status
     RETURNING {READ_PARAMS}
    """
    params: dict[str, Any] = {
        "account_id": account_id,
        "new_status": Status.DELETED,
        "old_status": status,
    }
    rec = await ctx.db.fetch_one(query, params)
    return rec
