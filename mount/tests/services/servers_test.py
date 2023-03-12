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
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert data2 == ServiceError.SERVERS_NAME_ALREADY_EXISTS


async def test_should_fetch_one_server_by_id(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.fetch_one(ctx, server_id=data["server_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["server_name"] == "Akatsuki"
    assert data2["hourly_request_limit"] == 100


async def test_should_fetch_one_server_by_name(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.fetch_one(ctx, server_name="Akatsuki")
    assert not isinstance(data2, ServiceError)
    assert data2["server_name"] == "Akatsuki"
    assert data2["hourly_request_limit"] == 100


async def test_should_not_fetch_one_nonexistent_server(ctx: Context):
    data = await servers.fetch_one(ctx, server_id=1)
    assert data == ServiceError.SERVERS_NOT_FOUND


async def test_should_not_fetch_one_deleted_server(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.delete(ctx, server_id=data["server_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["server_name"] == "Akatsuki"
    assert data2["hourly_request_limit"] == 100

    data3 = await servers.fetch_one(ctx, server_id=1)
    assert data3 == ServiceError.SERVERS_NOT_FOUND


async def test_should_fetch_all_servers(ctx: Context):
    for server_name in ("Akatsuki", "Ripple", "Gatari"):
        data = await servers.create(
            ctx,
            server_name=server_name,
            hourly_request_limit=100,
        )
        assert not isinstance(data, ServiceError)
        assert data["server_name"] == server_name
        assert data["hourly_request_limit"] == 100

    data2 = await servers.fetch_many(ctx)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 3

    for server_data, expected_name in zip(data2, ("Akatsuki", "Ripple", "Gatari")):
        assert server_data["server_name"] == expected_name
        assert server_data["hourly_request_limit"] == 100


async def test_should_fetch_one_page_of_servers(ctx: Context):
    for server_name in ("Akatsuki", "Ripple", "Gatari"):
        data = await servers.create(
            ctx,
            server_name=server_name,
            hourly_request_limit=100,
        )
        assert not isinstance(data, ServiceError)
        assert data["server_name"] == server_name
        assert data["hourly_request_limit"] == 100

    data2 = await servers.fetch_many(ctx, page=1, page_size=2)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 2

    for server_data, expected_name in zip(data2, ("Akatsuki", "Ripple")):
        assert server_data["server_name"] == expected_name
        assert server_data["hourly_request_limit"] == 100


async def test_should_partial_update_server(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.partial_update(
        ctx,
        server_id=data["server_id"],
        server_name="Ripple",
        hourly_request_limit=200,
    )
    assert not isinstance(data2, ServiceError)
    assert data2["server_name"] == "Ripple"
    assert data2["hourly_request_limit"] == 200


async def test_should_not_partial_update_nonexistent_server(ctx: Context):
    data = await servers.partial_update(
        ctx,
        server_id=1,
        hourly_request_limit=200,
    )
    assert data == ServiceError.SERVERS_NOT_FOUND


async def test_should_not_partial_update_deleted_server(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.delete(ctx, server_id=data["server_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["server_name"] == "Akatsuki"
    assert data2["hourly_request_limit"] == 100

    data3 = await servers.partial_update(
        ctx,
        server_id=1,
        hourly_request_limit=200,
    )
    assert data3 == ServiceError.SERVERS_NOT_FOUND


async def test_should_delete_server(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.delete(ctx, server_id=data["server_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["server_name"] == "Akatsuki"
    assert data2["hourly_request_limit"] == 100


async def test_should_not_delete_nonexistent_server(ctx: Context):
    data = await servers.delete(ctx, server_id=2)
    assert data == ServiceError.SERVERS_NOT_FOUND


async def test_should_not_delete_deleted_server(ctx: Context):
    data = await servers.create(
        ctx,
        server_name="Akatsuki",
        hourly_request_limit=100,
    )
    assert not isinstance(data, ServiceError)
    assert data["server_name"] == "Akatsuki"
    assert data["hourly_request_limit"] == 100

    data2 = await servers.delete(ctx, server_id=data["server_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["server_name"] == "Akatsuki"
    assert data2["hourly_request_limit"] == 100

    data3 = await servers.delete(ctx, server_id=1)
    assert data3 == ServiceError.SERVERS_NOT_FOUND
