import uuid
from typing import Any
from uuid import UUID

from app.common import formatters
from app.common import validators
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories import login_attempts as login_attempts_repo


async def create(
    ctx: Context,
    phone_number: str,
    ip_address: str,
    user_agent: str,
) -> dict[str, Any] | ServiceError:
    if not validators.validate_phone_number(phone_number):
        return ServiceError.LOGIN_ATTEMPTS_PHONE_NUMBER_INVALID

    login_attempt_id = uuid.uuid4()
    phone_number = formatters.phone_number(phone_number)

    login_attempt = await login_attempts_repo.create(
        ctx,
        login_attempt_id,
        phone_number,
        ip_address,
        user_agent,
    )

    return login_attempt


async def fetch_one(
    ctx: Context,
    login_attempt_id: UUID,
) -> dict[str, Any] | ServiceError:
    login_attempt = await login_attempts_repo.fetch_one(ctx, login_attempt_id)

    if login_attempt is None:
        return ServiceError.LOGIN_ATTEMPTS_NOT_FOUND

    return login_attempt


async def fetch_many(
    ctx: Context,
    phone_number: str | None = None,
    ip_address: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
) -> list[dict[str, Any]]:
    if phone_number is not None:
        phone_number = formatters.phone_number(phone_number)

    login_attempts = await login_attempts_repo.fetch_many(
        ctx,
        phone_number,
        ip_address,
        page,
        page_size,
    )

    return login_attempts
