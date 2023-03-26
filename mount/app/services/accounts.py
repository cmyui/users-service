import uuid
from typing import Any
from uuid import UUID

import phonenumbers
from app.common import security
from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories import accounts as accounts_repo
from app.validators import accounts as accounts_validator


def format_phone_number(phone_number: str) -> str:
    return phonenumbers.format_number(
        numobj=phonenumbers.parse(phone_number),
        num_format=phonenumbers.PhoneNumberFormat.E164,
    )


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

    account_id = uuid.uuid4()
    hashed_password = security.hash_password(password)
    formatted_phone_number = format_phone_number(phone_number)
    account = await accounts_repo.create(
        ctx,
        account_id,
        formatted_phone_number,
        hashed_password,
        first_name,
        last_name,
    )

    return account


async def fetch_one(
    ctx: Context,
    account_id: UUID | None = None,
    phone_number: str | None = None,
) -> dict[str, Any] | ServiceError:
    if phone_number is not None:
        phone_number = format_phone_number(phone_number)

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
        phone_number = format_phone_number(phone_number)

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
    account = await accounts_repo.delete(ctx, account_id)

    if account is None:
        return ServiceError.ACCOUNTS_NOT_FOUND

    return account
