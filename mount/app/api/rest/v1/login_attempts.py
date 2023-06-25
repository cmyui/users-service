from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.login_attempts import LoginAttempt
from app.services import login_attempts
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query

router = APIRouter(tags=["Login Attempts"])


@router.get("/v1/login-attempts/{login_attempt_id}")
async def fetch_one(
    login_attempt_id: UUID,
    ctx: RequestContext = Depends(),
) -> Success[LoginAttempt]:
    data = await login_attempts.fetch_one(ctx, login_attempt_id=login_attempt_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get account")

    resp = LoginAttempt.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/login-attempts")
async def fetch_many(
    username: str | None = None,
    ip_address: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    ctx: RequestContext = Depends(),
) -> Success[list[LoginAttempt]]:
    data = await login_attempts.fetch_many(
        ctx,
        username=username,
        ip_address=ip_address,
        page=page,
        page_size=page_size,
    )
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get accounts")

    resp = [LoginAttempt.from_mapping(d) for d in data]
    return responses.success(
        resp,
        meta={
            "total": len(resp),
            "page_size": page_size,
            "page": page,
        },
    )
