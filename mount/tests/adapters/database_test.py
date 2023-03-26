from app.adapters import database
from app.common import settings
from app.common.context import Context


def test_should_create_pool():
    pool = database._create_pool(
        dsn="postgresql+asyncpg://user:password@host:5432/database",
        min_pool_size=1,
        max_pool_size=10,
        ssl=True,
    )
    assert pool
    assert pool.url.dialect == "postgresql"
    assert pool.url.driver == "asyncpg"
    assert pool.url.username == "user"
    assert pool.url.password == "password"
    assert pool.url.hostname == "host"
    assert pool.url.port == 5432
    assert pool.url.database == "database"
    assert pool.options["min_size"] == 1
    assert pool.options["max_size"] == 10
    assert pool.options["ssl"] is True


def test_should_create_dsn():
    dsn = database.dsn(
        scheme="postgresql+asyncpg",
        user="user",
        password="password",
        host="host",
        port=5432,
        database="database",
    )
    assert dsn == "postgresql+asyncpg://user:password@host:5432/database"


async def test_should_connect_and_disconnect_from_database() -> None:
    db = database.ServiceDatabase(
        write_dsn=database.dsn(
            scheme=settings.WRITE_DB_SCHEME,
            user=settings.WRITE_DB_USER,
            password=settings.WRITE_DB_PASS,
            host=settings.WRITE_DB_HOST,
            port=settings.WRITE_DB_PORT,
            database=settings.WRITE_DB_NAME,
        ),
        read_dsn=database.dsn(
            scheme=settings.WRITE_DB_SCHEME,
            user=settings.READ_DB_USER,
            password=settings.READ_DB_PASS,
            host=settings.READ_DB_HOST,
            port=settings.READ_DB_PORT,
            database=settings.READ_DB_NAME,
        ),
        min_pool_size=settings.MIN_DB_POOL_SIZE,
        max_pool_size=settings.MAX_DB_POOL_SIZE,
        ssl=settings.DB_USE_SSL,
    )
    assert not db.read_pool.is_connected
    assert not db.write_pool.is_connected

    await db.connect()
    assert db.read_pool.is_connected
    assert db.write_pool.is_connected

    await db.disconnect()
    assert not db.read_pool.is_connected
    assert not db.write_pool.is_connected


async def test_should_create_connection() -> None:
    db = database.ServiceDatabase(
        write_dsn=database.dsn(
            scheme=settings.WRITE_DB_SCHEME,
            user=settings.WRITE_DB_USER,
            password=settings.WRITE_DB_PASS,
            host=settings.WRITE_DB_HOST,
            port=settings.WRITE_DB_PORT,
            database=settings.WRITE_DB_NAME,
        ),
        read_dsn=database.dsn(
            scheme=settings.WRITE_DB_SCHEME,
            user=settings.READ_DB_USER,
            password=settings.READ_DB_PASS,
            host=settings.READ_DB_HOST,
            port=settings.READ_DB_PORT,
            database=settings.READ_DB_NAME,
        ),
        min_pool_size=settings.MIN_DB_POOL_SIZE,
        max_pool_size=settings.MAX_DB_POOL_SIZE,
        ssl=settings.DB_USE_SSL,
    )
    await db.connect()

    conn = db.connection()
    assert conn


async def test_should_create_transaction() -> None:
    db = database.ServiceDatabase(
        write_dsn=database.dsn(
            scheme=settings.WRITE_DB_SCHEME,
            user=settings.WRITE_DB_USER,
            password=settings.WRITE_DB_PASS,
            host=settings.WRITE_DB_HOST,
            port=settings.WRITE_DB_PORT,
            database=settings.WRITE_DB_NAME,
        ),
        read_dsn=database.dsn(
            scheme=settings.WRITE_DB_SCHEME,
            user=settings.READ_DB_USER,
            password=settings.READ_DB_PASS,
            host=settings.READ_DB_HOST,
            port=settings.READ_DB_PORT,
            database=settings.READ_DB_NAME,
        ),
        min_pool_size=settings.MIN_DB_POOL_SIZE,
        max_pool_size=settings.MAX_DB_POOL_SIZE,
        ssl=settings.DB_USE_SSL,
    )

    tx = db.transaction()
    assert tx


# TODO: test actual usage of transactions?


# NOTE: from below here, we will rely on the db fixture from conftest.py


async def test_should_fetch_one_row(ctx: Context) -> None:
    result = await ctx.db.fetch_one("SELECT 123")
    assert result == {"?column?": 123}


async def test_should_fetch_all_rows(ctx: Context) -> None:
    result = await ctx.db.fetch_all("SELECT 123")
    assert result == [{"?column?": 123}]


async def test_should_fetch_val(ctx: Context) -> None:
    result = await ctx.db.fetch_val("SELECT 123")
    assert result == 123


async def test_should_execute_query(ctx: Context) -> None:
    result = await ctx.db.execute("SELECT 123")
    assert result == 123


async def test_should_execute_many_queries(ctx: Context) -> None:
    result = await ctx.db.execute_many(
        "SELECT :val",
        [
            {"val": "hello"},
            {"val": "world"},
        ],
    )
    assert result is None
