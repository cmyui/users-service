import traceback
import uuid
from typing import Any
from uuid import UUID

from app.common import formatters
from app.common import logger
from app.common import security
from app.common import validators
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories import accounts as accounts_repo
from app.repositories import credentials as credentials_repo


async def create(
    ctx: Context,
    phone_number: str,
    password: str,
    first_name: str,
    last_name: str,
) -> dict[str, Any] | ServiceError:
    if not validators.validate_phone_number(phone_number):
        return ServiceError.ACCOUNTS_PHONE_NUMBER_INVALID

    phone_number = formatters.phone_number(phone_number)

    if not validators.validate_password(password):
        return ServiceError.ACCOUNTS_PASSWORD_INVALID
    if await accounts_repo.fetch_one(ctx, phone_number=phone_number):
        return ServiceError.ACCOUNTS_PHONE_NUMBER_EXISTS

    account_id = uuid.uuid4()
    hashed_password = security.hash_password(password)

    transaction = await ctx.db.transaction()

    try:
        account = await accounts_repo.create(
            ctx,
            account_id,
            phone_number,
            hashed_password,
            first_name,
            last_name,
        )

        await credentials_repo.create(
            ctx,
            account_id,
            phone_number,
            hashed_password,
        )
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
    account_id: UUID | None = None,
    phone_number: str | None = None,
) -> dict[str, Any] | ServiceError:
    if phone_number is not None:
        phone_number = formatters.phone_number(phone_number)

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
    account_id: UUID,
    phone_number: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> dict[str, Any] | ServiceError:
    if phone_number is not None:
        phone_number = formatters.phone_number(phone_number)

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
    account_id: UUID,
) -> dict[str, Any] | ServiceError:
    transaction = await ctx.db.transaction()

    try:
        account = await accounts_repo.delete(ctx, account_id)

        if account is None:
            return ServiceError.ACCOUNTS_NOT_FOUND

        all_credentials = await credentials_repo.fetch_many(ctx, account_id=account_id)
        for credentials in all_credentials:
            deleted_credentials = await credentials_repo.delete(
                ctx,
                credentials["credential_id"],
            )
            if deleted_credentials is None:  # pragma: no cover
                raise RuntimeError("Unable to delete credentials")

    except Exception as exc:  # pragma: no cover
        await transaction.rollback()
        logger.error("Unable to delete account:", error=exc)
        logger.error("Stack trace: ", error=traceback.format_exc())
        return ServiceError.ACCOUNTS_DELETION_FAILED
    else:
        await transaction.commit()

    return account
