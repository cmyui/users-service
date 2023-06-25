from uuid import UUID

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.sessions import LoginForm
from app.models.sessions import Session
from app.models.sessions import SessionUpdate
from app.services import sessions
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import Query
from fastapi import status

router = APIRouter(tags=["Sessions"])


@router.post(
    "/v1/sessions",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    args: LoginForm,
    cf_connecting_ip: str = Header("CF-Connecting-IP"),
    user_agent: str = Header("User-Agent"),
    ctx: RequestContext = Depends(),
) -> Success[Session]:
    data = await sessions.create(
        ctx,
        args.username,
        args.password,
        cf_connecting_ip,
        user_agent,
    )
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create session")

    resp = Session.from_mapping(data)
    return responses.success(
        content=resp,
        status_code=status.HTTP_201_CREATED,
        headers={
            "Location": f"/v1/sessions/{resp.session_id}",
        },
    )


@router.get("/v1/sessions/{session_id}")
async def fetch_one(
    session_id: UUID,
    ctx: RequestContext = Depends(),
) -> Success[Session]:
    data = await sessions.fetch_one(ctx, session_id=session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get session")

    resp = Session.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/sessions")
async def fetch_many(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    ctx: RequestContext = Depends(),
) -> Success[list[Session]]:
    data = await sessions.fetch_many(ctx, page=page, page_size=page_size)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get sessions")

    resp = [Session.from_mapping(d) for d in data]
    return responses.success(
        resp,
        meta={
            "total": len(resp),
            "page_size": page_size,
            "page": page,
        },
    )


@router.patch("/v1/sessions/{session_id}")
async def partial_update(
    session_id: UUID,
    args: SessionUpdate,
    ctx: RequestContext = Depends(),
) -> Success[Session]:
    data = await sessions.partial_update(
        ctx,
        session_id,
        expires_at=args.expires_at,
    )
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update session")

    resp = Session.from_mapping(data)
    return responses.success(resp)


@router.delete(
    "/v1/sessions/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    session_id: UUID,
    ctx: RequestContext = Depends(),
) -> None:
    data = await sessions.delete(ctx, session_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete session")

    return responses.no_content()
