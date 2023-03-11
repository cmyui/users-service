from app.common.context import Context
from app.common.errors import ServiceError
from app.services import servers


async def test_should_create_server(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100


async def test_should_not_create_server_with_preexisting_name(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert data == ServiceError.SERVERS_NAME_ALREADY_EXISTS


async def test_should_fetch_one_server(ctx: Context):
    data = await servers.fetch_one(ctx, server_id=1)
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100


async def test_should_not_fetch_one_server(ctx: Context):
    data = await servers.fetch_one(ctx, server_id=2)
    assert data == ServiceError.SERVERS_NOT_FOUND


async def test_should_fetch_many_servers(ctx: Context):
    data = await servers.fetch_many(ctx)
    assert not isinstance(data, ServiceError)
    assert len(data) == 1
    assert data[0]["server_name"] == "Akatsuki"
    assert data[0]["hourly_request_limit"] == 100


async def test_should_partial_update_server(ctx: Context):
    data = await servers.partial_update(
        ctx,
        server_id=1,
        hourly_request_limit=200,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 200


async def test_should_not_partial_update_server(ctx: Context):
    data = await servers.partial_update(
        ctx,
        server_id=2,
        hourly_request_limit=200,
    )
    assert data == ServiceError.SERVERS_NOT_FOUND


async def test_should_delete_server(ctx: Context):
    data = await servers.delete(ctx, server_id=1)
    assert not isinstance(data, ServiceError)


async def test_should_not_delete_server(ctx: Context):
    data = await servers.delete(ctx, server_id=2)
    assert data == ServiceError.SERVERS_NOT_FOUND
