from typing import Any
from uuid import UUID

from app.common.context import Context

READ_PARAMS = """\
    login_attempt_id, phone_number, ip_address, user_agent, created_at
"""


async def create(
    ctx: Context,
    login_attempt_id: UUID,
    phone_number: str,
    ip_address: str,
    user_agent: str,
) -> dict[str, Any]:
    query = f"""\
        INSERT INTO login_attempts (login_attempt_id, phone_number, ip_address,
                                    user_agent)
             VALUES (:login_attempt_id, :phone_number, :ip_address,
                     :user_agent)
          RETURNING {READ_PARAMS}
    """
    params: dict[str, Any] = {
        "login_attempt_id": login_attempt_id,
        "phone_number": phone_number,
        "ip_address": ip_address,
        "user_agent": user_agent,
    }

    rec = await ctx.db.fetch_one(query, params)
    assert rec is not None
    return rec


async def fetch_one(
    ctx: Context,
    login_attempt_id: UUID | None = None,
) -> dict[str, Any] | None:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM login_attempts
         WHERE login_attempt_id = :login_attempt_id
    """
    params: dict[str, Any] = {
        "login_attempt_id": login_attempt_id,
    }

    rec = await ctx.db.fetch_one(query, params)

    if rec is None:
        return None

    return rec


async def fetch_many(
    ctx: Context,
    phone_number: str | None = None,
    ip_address: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> list[dict[str, Any]]:
    query = f"""\
        SELECT {READ_PARAMS}
          FROM login_attempts
         WHERE phone_number = COALESCE(:phone_number, phone_number)
           AND ip_address = COALESCE(:ip_address, ip_address)
    """
    params: dict[str, Any] = {
        "phone_number": phone_number,
        "ip_address": ip_address,
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
