import uuid
from datetime import datetime
from typing import Any
from uuid import UUID

from app.common import formatters
from app.common import security
from app.common import validators
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories import login_attempts as login_attempts_repo
from app.repositories import sessions as sessions_repo
from app.repositories import accounts as accounts_repo


async def create(
    ctx: Context,
    username: str,
    password: str,
    ip_address: str,
    user_agent: str,
) -> dict[str, Any] | ServiceError:
    login_attempt_id = uuid.uuid4()
    await login_attempts_repo.create(
        ctx,
        login_attempt_id,
        username,
        ip_address,
        user_agent,
    )

    if not validators.validate_username(username):
        return ServiceError.SESSIONS_USERNAME_INVALID

    if not validators.validate_password(password):
        return ServiceError.SESSIONS_PASSWORD_INVALID

    account = await accounts_repo.fetch_one(ctx, username=username)

    if account is None:
        return ServiceError.CREDENTIALS_INCORRECT

    if not security.verify_password(
        hashed_password=account["hashed_password"],
        password=password,
    ):
        return ServiceError.CREDENTIALS_INCORRECT

    session_id = uuid.uuid4()

    session = await sessions_repo.create(
        ctx,
        session_id,
        account["account_id"],
    )

    return session


async def fetch_one(
    ctx: Context,
    session_id: UUID,
) -> dict[str, Any] | ServiceError:
    session = await sessions_repo.fetch_one(ctx, session_id)

    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    return session


async def fetch_many(
    ctx: Context,
    account_id: UUID | None = None,
    page: int = 1,
    page_size: int = 50,
) -> list[dict[str, Any]]:
    sessions = await sessions_repo.fetch_many(ctx, account_id, page, page_size)
    return sessions


async def partial_update(
    ctx: Context,
    session_id: UUID,
    expires_at: datetime | None = None,
) -> dict[str, Any] | ServiceError:
    session = await sessions_repo.partial_update(
        ctx,
        session_id,
        expires_at=expires_at,
    )

    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    return session


async def delete(
    ctx: Context,
    session_id: UUID,
) -> dict[str, Any] | ServiceError:
    session = await sessions_repo.delete(ctx, session_id)

    if session is None:
        return ServiceError.SESSIONS_NOT_FOUND

    return session
