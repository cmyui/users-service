from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Literal
from uuid import UUID

from app.common import json
from app.common import logger
from app.common.context import Context

SESSION_EXPIRY = 3600  # 1h


def create_session_key(session_id: UUID | Literal["*"]) -> str:
    return f"users:sessions:{session_id}"


# TODO: is my usage of setex correct?
# i'm technically desyncing from the expires_at var


async def create(
    ctx: Context,
    session_id: UUID,
    account_id: UUID,
) -> dict[str, Any]:
    now = datetime.now()
    expires_at = now + timedelta(seconds=SESSION_EXPIRY)
    session = {
        "session_id": str(session_id),
        "account_id": str(account_id),
        "expires_at": expires_at.isoformat(),
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }
    await ctx.redis.setex(
        name=create_session_key(session_id),
        time=SESSION_EXPIRY,
        value=json.dumps(session),
    )
    return session


async def fetch_one(ctx: Context, session_id: UUID) -> dict[str, Any] | None:
    session = await ctx.redis.get(create_session_key(session_id))
    if session is None:
        return None
    return json.loads(session)


async def fetch_many(
    ctx: Context,
    account_id: UUID | None = None,
    page: int = 1,
    page_size: int = 50,
) -> list[dict[str, Any]]:
    session_key = create_session_key("*")

    if page > 1:
        cursor, keys = await ctx.redis.scan(
            cursor=0,
            match=session_key,
            count=(page - 1) * page_size,
        )
    else:
        cursor = None

    sessions = []
    while cursor != 0:
        cursor, keys = await ctx.redis.scan(
            cursor=cursor or 0,
            match=session_key,
            count=page_size,
        )

        raw_sessions = await ctx.redis.mget(keys)
        for raw_session in raw_sessions:
            if raw_session is None:
                logger.warning("Session not found in Redis")
                continue

            session = json.loads(raw_session)

            if account_id is not None and session["account_id"] != str(account_id):
                continue

            sessions.append(session)

    # redis does not guarantee the count of keys returned
    # https://redis.io/commands/scan/#the-count-option
    return sessions[:page_size]


async def partial_update(
    ctx: Context,
    session_id: UUID,
    **kwargs: Any,
) -> dict[str, Any] | None:
    raw_session = await ctx.redis.get(create_session_key(session_id))
    if raw_session is None:
        return None

    session = json.loads(raw_session)

    if not kwargs:
        return session

    session = dict(session)

    expires_at = kwargs.get("expires_at")

    if expires_at is not None:
        session["expires_at"] = expires_at.isoformat()

    session["updated_at"] = datetime.now().isoformat()

    await ctx.redis.set(create_session_key(session_id), json.dumps(session))

    if expires_at is not None:
        await ctx.redis.expireat(create_session_key(session_id), expires_at)

    return session


async def delete(ctx: Context, session_id: UUID) -> dict[str, Any] | None:
    session_key = create_session_key(session_id)

    session = await ctx.redis.get(session_key)
    if session is None:
        return None

    await ctx.redis.delete(session_key)

    return json.loads(session)
