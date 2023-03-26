from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.servers import Server
from app.models.servers import ServerInput
from app.models.servers import ServerUpdate
from app.services import servers
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status

router = APIRouter(tags=["Servers"])


@router.post(
    "/v1/servers",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    args: ServerInput,
    ctx: RequestContext = Depends(),
) -> Success[Server]:
    data = await servers.create(
        ctx,
        args.server_name,
        args.hourly_request_limit,
    )
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create server")

    resp = Server.from_mapping(data)
    return responses.success(
        content=resp,
        status_code=status.HTTP_201_CREATED,
        headers={
            "Location": f"/v1/servers/{resp.server_id}",
        },
    )


@router.get("/v1/servers/{server_id}")
async def fetch_one(
    server_id: int,
    ctx: RequestContext = Depends(),
) -> Success[Server]:
    data = await servers.fetch_one(ctx, server_id=server_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get server")

    resp = Server.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/servers")
async def fetch_many(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
    ctx: RequestContext = Depends(),
) -> Success[list[Server]]:
    data = await servers.fetch_many(ctx, page=page, page_size=page_size)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to get servers")

    resp = [Server.from_mapping(d) for d in data]
    return responses.success(
        resp,
        meta={
            "total": len(resp),
            "page_size": page_size,
            "page": page,
        },
    )


@router.patch("/v1/servers/{server_id}")
async def partial_update(
    server_id: int,
    args: ServerUpdate,
    ctx: RequestContext = Depends(),
) -> Success[Server]:
    data = await servers.partial_update(
        ctx,
        server_id,
        server_name=args.server_name,
        hourly_request_limit=args.hourly_request_limit,
    )
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update server")

    resp = Server.from_mapping(data)
    return responses.success(resp)


@router.delete(
    "/v1/servers/{server_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    server_id: int,
    ctx: RequestContext = Depends(),
) -> None:
    data = await servers.delete(ctx, server_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete server")

    return responses.no_content()
