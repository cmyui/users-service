import uuid
from datetime import datetime
from datetime import timedelta

from app.common import formatters
from app.common.context import Context
from app.common.errors import ServiceError
from app.services import accounts
from app.services import sessions
from testing import sample_data


async def test_should_create_session(ctx: Context):
    phone_number = sample_data.fake_phone_number()
    password = sample_data.fake_password()
    first_name = sample_data.fake_first_name()
    last_name = sample_data.fake_last_name()

    data = await accounts.create(
        ctx,
        phone_number=phone_number,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data
    assert data["first_name"] == first_name
    assert data["last_name"] == last_name

    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data2 = await sessions.create(
        ctx,
        phone_number=phone_number,
        password=password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data2, ServiceError)
    assert data2.keys() == {
        "session_id",
        "account_id",
        "expires_at",
        "created_at",
        "updated_at",
    }


async def test_should_not_create_session_with_invalid_phone_number(ctx: Context):
    data = await sessions.create(
        ctx,
        phone_number="15555555555",
        password=sample_data.fake_password(),
        ip_address=sample_data.fake_ipv4_address(),
        user_agent=sample_data.fake_user_agent(),
    )
    assert data == ServiceError.SESSIONS_PHONE_NUMBER_INVALID


async def test_should_not_create_session_with_invalid_password(ctx: Context):
    data = await sessions.create(
        ctx,
        phone_number=sample_data.fake_phone_number(),
        password="abc",
        ip_address=sample_data.fake_ipv4_address(),
        user_agent=sample_data.fake_user_agent(),
    )
    assert data == ServiceError.SESSIONS_PASSWORD_INVALID


async def test_should_fetch_one_session(ctx: Context):
    phone_number = sample_data.fake_phone_number()
    password = sample_data.fake_password()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await sessions.create(
        ctx,
        phone_number=phone_number,
        password=password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data.keys() == {
        "session_id",
        "account_id",
        "expires_at",
        "created_at",
        "updated_at",
    }

    data2 = await sessions.fetch_one(ctx, session_id=data["session_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["session_id"] == data["session_id"]
    assert data2["account_id"] == data["account_id"]
    assert data2["expires_at"] == data["expires_at"]
    assert data2["created_at"] == data["created_at"]
    assert data2["updated_at"] == data["updated_at"]


async def test_should_not_fetch_one_nonexistent_session(ctx: Context):
    data = await sessions.fetch_one(ctx, session_id=uuid.uuid4())
    assert data == ServiceError.SESSIONS_NOT_FOUND


async def test_should_not_fetch_one_deleted_session(ctx: Context):
    phone_number = sample_data.fake_phone_number()
    password = sample_data.fake_password()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await sessions.create(
        ctx,
        phone_number=phone_number,
        password=password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data.keys() == {
        "session_id",
        "account_id",
        "expires_at",
        "created_at",
        "updated_at",
    }

    data2 = await sessions.delete(ctx, session_id=data["session_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["session_id"] == data["session_id"]
    assert data2["account_id"] == data["account_id"]
    assert data2["expires_at"] == data["expires_at"]
    assert data2["created_at"] == data["created_at"]
    assert data2["updated_at"] == data["updated_at"]

    data3 = await sessions.fetch_one(ctx, session_id=data["session_id"])
    assert data3 == ServiceError.SESSIONS_NOT_FOUND


async def test_should_fetch_all_sessions(ctx: Context):
    expected = []
    for _ in range(3):
        phone_number = sample_data.fake_phone_number()
        password = sample_data.fake_password()
        ip_address = sample_data.fake_ipv4_address()
        user_agent = sample_data.fake_user_agent()

        data = await sessions.create(
            ctx,
            phone_number=phone_number,
            password=password,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        assert not isinstance(data, ServiceError)
        assert data.keys() == {
            "session_id",
            "account_id",
            "expires_at",
            "created_at",
            "updated_at",
        }

        expected.append(data)

    data2 = await sessions.fetch_many(ctx)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 3

    for account_data, expected_data in zip(data2, expected):
        assert account_data["session_id"] == expected_data["session_id"]
        assert account_data["account_id"] == expected_data["account_id"]
        assert account_data["expires_at"] == expected_data["expires_at"]
        assert account_data["created_at"] == expected_data["created_at"]
        assert account_data["updated_at"] == expected_data["updated_at"]


async def test_should_fetch_one_page_of_sessions(ctx: Context):
    expected = []
    for _ in range(3):
        phone_number = sample_data.fake_phone_number()
        password = sample_data.fake_password()
        ip_address = sample_data.fake_ipv4_address()
        user_agent = sample_data.fake_user_agent()

        data = await sessions.create(
            ctx,
            phone_number=phone_number,
            password=password,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        assert not isinstance(data, ServiceError)
        assert data.keys() == {
            "session_id",
            "account_id",
            "expires_at",
            "created_at",
            "updated_at",
        }

    data2 = await sessions.fetch_many(ctx, page=1, page_size=2)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 2

    for account_data, expected_data in zip(data2, expected):
        assert account_data["session_id"] == expected_data["session_id"]
        assert account_data["account_id"] == expected_data["account_id"]
        assert account_data["expires_at"] == expected_data["expires_at"]
        assert account_data["created_at"] == expected_data["created_at"]
        assert account_data["updated_at"] == expected_data["updated_at"]


async def test_should_partial_update_account(ctx: Context):
    phone_number = sample_data.fake_phone_number()
    password = sample_data.fake_password()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await sessions.create(
        ctx,
        phone_number=phone_number,
        password=password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data
    assert data["ip_address"] == ip_address
    assert data["user_agent"] == user_agent

    expires_at = datetime.utcnow() + timedelta(days=1)

    data2 = await sessions.partial_update(
        ctx,
        session_id=data["session_id"],
        expires_at=expires_at,
    )
    assert not isinstance(data2, ServiceError)
    assert data2["session_id"] == data["session_id"]
    assert data2["account_id"] == data["account_id"]
    assert data2["expires_at"] == expires_at
    assert data2["created_at"] == data["created_at"]
    assert data2["updated_at"] > data["updated_at"]


async def test_should_not_partial_update_nonexistent_account(ctx: Context):
    expires_at = datetime.utcnow() + timedelta(days=1)

    data = await sessions.partial_update(
        ctx,
        session_id=uuid.uuid4(),
        expires_at=expires_at,
    )
    assert data == ServiceError.SESSIONS_NOT_FOUND


async def test_should_not_partial_update_deleted_account(ctx: Context):
    phone_number = sample_data.fake_phone_number()
    password = sample_data.fake_password()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await sessions.create(
        ctx,
        phone_number=phone_number,
        password=password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data.keys() == {
        "session_id",
        "account_id",
        "expires_at",
        "created_at",
        "updated_at",
    }

    data2 = await sessions.delete(ctx, session_id=data["session_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["session_id"] == data["session_id"]
    assert data2["account_id"] == data["account_id"]
    assert data2["expires_at"] == data["expires_at"]
    assert data2["created_at"] == data["created_at"]
    assert data2["updated_at"] > data["updated_at"]

    expires_at = datetime.utcnow() + timedelta(days=1)

    data3 = await sessions.partial_update(
        ctx,
        session_id=data["session_id"],
        expires_at=expires_at,
    )
    assert data3 == ServiceError.SESSIONS_NOT_FOUND


async def test_should_delete_account(ctx: Context):
    phone_number = sample_data.fake_phone_number()
    password = sample_data.fake_password()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await sessions.create(
        ctx,
        phone_number=phone_number,
        password=password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data.keys() == {
        "session_id",
        "account_id",
        "expires_at",
        "created_at",
        "updated_at",
    }

    data2 = await sessions.delete(ctx, session_id=data["session_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["session_id"] == data["session_id"]
    assert data2["account_id"] == data["account_id"]
    assert data2["expires_at"] == data["expires_at"]
    assert data2["created_at"] == data["created_at"]
    assert data2["updated_at"] > data["updated_at"]


async def test_should_not_delete_nonexistent_account(ctx: Context):
    data = await sessions.delete(ctx, session_id=uuid.uuid4())
    assert data == ServiceError.SESSIONS_NOT_FOUND


async def test_should_not_delete_deleted_account(ctx: Context):
    phone_number = sample_data.fake_phone_number()
    password = sample_data.fake_password()
    ip_address = sample_data.fake_ipv4_address()
    user_agent = sample_data.fake_user_agent()

    data = await sessions.create(
        ctx,
        phone_number=phone_number,
        password=password,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    assert not isinstance(data, ServiceError)
    assert data.keys() == {
        "session_id",
        "account_id",
        "expires_at",
        "created_at",
        "updated_at",
    }

    data2 = await sessions.delete(ctx, session_id=data["session_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["session_id"] == data["session_id"]
    assert data2["account_id"] == data["account_id"]
    assert data2["expires_at"] == data["expires_at"]
    assert data2["created_at"] == data["created_at"]
    assert data2["updated_at"] > data["updated_at"]

    data3 = await sessions.delete(ctx, session_id=data["session_id"])
    assert data3 == ServiceError.SESSIONS_NOT_FOUND
