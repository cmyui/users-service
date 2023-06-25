import uuid

from app.common import formatters
from app.common.context import Context
from app.common.errors import ServiceError
from app.services import login_attempts
from testing import sample_data


async def test_should_create_login_attempt(ctx: Context):
    username = sample_data.fake_username()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await login_attempts.create(
        ctx,
        username=username,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data["username"] == username
    assert data["ip_address"] == ip_address
    assert data["user_agent"] == user_agent


async def test_should_not_create_login_attempt_with_invalid_username(ctx: Context):
    data = await login_attempts.create(
        ctx,
        username="12",
        ip_address=sample_data.fake_ipv4_address(),
        user_agent=sample_data.fake_user_agent(),
    )
    assert data is ServiceError.LOGIN_ATTEMPTS_USERNAME_INVALID


async def test_should_fetch_one_login_attempt_by_id(ctx: Context):
    username = sample_data.fake_username()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await login_attempts.create(
        ctx,
        username=username,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data["username"] == username
    assert data["ip_address"] == ip_address
    assert data["user_agent"] == user_agent

    data2 = await login_attempts.fetch_one(
        ctx, login_attempt_id=data["login_attempt_id"]
    )
    assert not isinstance(data2, ServiceError)
    assert data2["username"] == username
    assert data2["ip_address"] == ip_address
    assert data2["user_agent"] == user_agent


async def test_should_not_fetch_one_nonexistent_login_attempt(ctx: Context):
    data = await login_attempts.fetch_one(ctx, login_attempt_id=uuid.uuid4())
    assert data is ServiceError.LOGIN_ATTEMPTS_NOT_FOUND


async def test_should_fetch_all_login_attempts(ctx: Context):
    expected = []
    for _ in range(3):
        username = sample_data.fake_username()
        ip_address = sample_data.fake_ipv4_address()
        user_agent = sample_data.fake_user_agent()

        data = await login_attempts.create(
            ctx,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        assert not isinstance(data, ServiceError)
        assert data["username"] == username
        assert data["ip_address"] == ip_address
        assert data["user_agent"] == user_agent

        expected.append(data)

    data2 = await login_attempts.fetch_many(ctx)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 3

    for account_data, expected_data in zip(data2, expected):
        assert account_data["username"] == expected_data["username"]
        assert account_data["ip_address"] == expected_data["ip_address"]
        assert account_data["user_agent"] == expected_data["user_agent"]


async def test_should_fetch_one_page_of_login_attempts(ctx: Context):
    expected = []
    for _ in range(3):
        username = sample_data.fake_username()
        ip_address = sample_data.fake_ipv4_address()
        user_agent = sample_data.fake_user_agent()

        data = await login_attempts.create(
            ctx,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        assert not isinstance(data, ServiceError)
        assert data["username"] == username
        assert data["ip_address"] == ip_address
        assert data["user_agent"] == user_agent

        expected.append(data)

    data2 = await login_attempts.fetch_many(ctx, page=1, page_size=2)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 2

    for account_data, expected_data in zip(data2, expected[:2]):
        assert account_data["username"] == expected_data["username"]
        assert account_data["ip_address"] == expected_data["ip_address"]
        assert account_data["user_agent"] == expected_data["user_agent"]
