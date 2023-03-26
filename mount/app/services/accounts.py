import traceback
from typing import Any

from app.common import logger
from app.common import security
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories import accounts as accounts_repo
from app.validators import accounts as accounts_validator


async def create(
    ctx: Context,
    phone_number: str,
    password: str,
    first_name: str,
    last_name: str,
) -> dict[str, Any] | ServiceError:
    if not accounts_validator.validate_phone_number(phone_number):
        return ServiceError.ACCOUNTS_PHONE_NUMBER_INVALID
    if not accounts_validator.validate_password(password):
        return ServiceError.ACCOUNTS_PASSWORD_INVALID
    if await accounts_repo.fetch_one(ctx, phone_number=phone_number):
        return ServiceError.ACCOUNTS_PHONE_NUMBER_EXISTS

    hashed_password = security.hash_password(password)

    transaction = await ctx.db.transaction()

    try:
        # TODO: split credentials into a separate table
        account = await accounts_repo.create(
            ctx,
            phone_number,
            hashed_password,
            first_name,
            last_name,
        )

        # TODO: store credentials separately
        # TODO: store login attempts

    except Exception as exc:  # pragma: no cover
        await transaction.rollback()
        logger.error("Unable to create account:", error=exc)
        logger.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.ACCOUNTS_CREATION_FAILED
    else:
        await transaction.commit()

    return account


async def fetch_one(
    ctx: Context,
    account_id: int | None = None,
    phone_number: str | None = None,
) -> dict[str, Any] | ServiceError:
    account = await accounts_repo.fetch_one(ctx, account_id, phone_number)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def fetch_many(
    ctx: Context,
    page: int | None = None,
    page_size: int | None = None,
) -> list[dict[str, Any]]:
    accounts = await accounts_repo.fetch_many(ctx, page, page_size)
    return accounts


async def partial_update(
    ctx: Context,
    account_id: int,
    phone_number: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> dict[str, Any] | ServiceError:
    account = await accounts_repo.partial_update(
        ctx,
        account_id,
        phone_number,
        first_name,
        last_name,
    )

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account


async def delete(
    ctx: Context,
    account_id: int,
) -> dict[str, Any] | ServiceError:
    account = await accounts_repo.delete(ctx, account_id)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account
