from typing import Annotated
from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.accounts import Account
from app.models.accounts import AccountUpdate
from app.models.accounts import SignupForm
from app.services import accounts
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status

router = APIRouter(tags=["Accounts"])


@router.post(
    "/v1/accounts",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    ctx: Annotated[RequestContext, Depends()],
    args: SignupForm,
) -> Success[Account]:
    data = await accounts.create(
        ctx,
        args.phone_number,
        args.password,
        args.first_name,
        args.last_name,
    )
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create account")

    resp = Account.from_mapping(data)
    return responses.success(
        content=resp,
        status_code=status.HTTP_201_CREATED,
        headers={
            "Location": f"/v1/accounts/{resp.account_id}",
        },
    )


@router.get("/v1/accounts/{account_id}")
async def fetch_one(
    ctx: Annotated[RequestContext, Depends()],
    account_id: UUID,
) -> Success[Account]:
    data = await accounts.fetch_one(ctx, account_id=account_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get account")

    resp = Account.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/accounts")
async def fetch_many(
    ctx: Annotated[RequestContext, Depends()],
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
) -> Success[list[Account]]:
    data = await accounts.fetch_many(ctx, page=page, page_size=page_size)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get accounts")

    resp = [Account.from_mapping(d) for d in data]
    return responses.success(
        resp,
        meta={
            "total": len(resp),
            "page_size": page_size,
            "page": page,
        },
    )


@router.patch("/v1/accounts/{account_id}")
async def partial_update(
    ctx: Annotated[RequestContext, Depends()],
    account_id: UUID,
    args: AccountUpdate,
) -> Success[Account]:
    data = await accounts.partial_update(
        ctx,
        account_id,
        phone_number=args.phone_number,
        first_name=args.first_name,
        last_name=args.last_name,
    )
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update account")

    resp = Account.from_mapping(data)
    return responses.success(resp)


@router.delete(
    "/v1/accounts/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    ctx: Annotated[RequestContext, Depends()],
    account_id: UUID,
) -> None:
    data = await accounts.delete(ctx, account_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete account")

    return responses.no_content()
