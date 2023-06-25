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
    username: str,
    password: str,
    first_name: str,
    last_name: str,
) -> dict[str, Any] | ServiceError:
    if not validators.validate_username(username):
        return ServiceError.ACCOUNTS_USERNAME_INVALID
    if not validators.validate_password(password):
        return ServiceError.ACCOUNTS_PASSWORD_INVALID
    if await accounts_repo.fetch_one(ctx, username=username):
        return ServiceError.ACCOUNTS_USERNAME_EXISTS

    transaction = await ctx.db.transaction()

    try:
        account_id = uuid.uuid4()

        account = await accounts_repo.create(
            ctx,
            account_id,
            username,
            first_name,
            last_name,
        )

        credentials_id = uuid.uuid4()
        hashed_password = security.hash_password(password)

        await credentials_repo.create(
            ctx,
            credentials_id,
            account_id,
            username,
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
    username: str | None = None,
) -> dict[str, Any] | ServiceError:
    account = await accounts_repo.fetch_one(
        ctx,
        account_id=account_id,
        username=username,
    )

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
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> dict[str, Any] | ServiceError:
    account = await accounts_repo.partial_update(
        ctx,
        account_id,
        username,
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
            await transaction.rollback()
            return ServiceError.ACCOUNTS_NOT_FOUND

        all_credentials = await credentials_repo.fetch_many(ctx, account_id=account_id)
        for credentials in all_credentials:
            deleted_credentials = await credentials_repo.delete(
                ctx,
                credentials["credentials_id"],
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
