import uuid

from app.common.context import Context
from app.common.errors import ServiceError
from app.services import accounts


async def test_should_create_account(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"


async def test_should_not_create_account_with_invalid_phone_number(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert data == ServiceError.ACCOUNTS_PHONE_NUMBER_INVALID


async def test_should_not_create_account_with_invalid_password(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="abc",
        first_name="John",
        last_name="Doe",
    )
    assert data == ServiceError.ACCOUNTS_PASSWORD_INVALID


async def test_should_not_create_account_with_preexisting_phone_number(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert data2 == ServiceError.ACCOUNTS_PHONE_NUMBER_EXISTS


async def test_should_fetch_one_account_by_id(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.fetch_one(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"


async def test_should_fetch_one_account_by_phone_number(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.fetch_one(ctx, phone_number="+15555555555")
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"


async def test_should_not_fetch_one_nonexistent_account(ctx: Context):
    data = await accounts.fetch_one(ctx, account_id=uuid.uuid4())
    assert data == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_fetch_one_deleted_account_by_id(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data3 = await accounts.fetch_one(ctx, account_id=data["account_id"])
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_fetch_one_deleted_account_by_phone_number(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data3 = await accounts.fetch_one(ctx, phone_number=data["phone_number"])
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_fetch_all_accounts(ctx: Context):
    for phone_number in (
        "+15555555555",
        "+15555555556",
        "+15555555557",
    ):
        data = await accounts.create(
            ctx,
            phone_number=phone_number,
            password="homeHome123$",
            first_name="John",
            last_name="Doe",
        )
        assert not isinstance(data, ServiceError)
        assert data["phone_number"] == phone_number

    data2 = await accounts.fetch_many(ctx)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 3

    for account_data, expected_phone_number in zip(
        data2,
        (
            "+15555555555",
            "+15555555556",
            "+15555555557",
        ),
    ):
        assert account_data["phone_number"] == expected_phone_number


async def test_should_fetch_one_page_of_accounts(ctx: Context):
    for phone_number in (
        "+15555555555",
        "+15555555556",
        "+15555555557",
    ):
        data = await accounts.create(
            ctx,
            phone_number=phone_number,
            password="homeHome123$",
            first_name="John",
            last_name="Doe",
        )
        assert not isinstance(data, ServiceError)
        assert data["phone_number"] == phone_number

    data2 = await accounts.fetch_many(ctx, page=1, page_size=2)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 2

    for account_data, expected_phone_number in zip(
        data2,
        (
            "+15555555555",
            "+15555555556",
        ),
    ):
        assert account_data["phone_number"] == expected_phone_number


async def test_should_partial_update_account(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.partial_update(
        ctx,
        account_id=data["account_id"],
        phone_number="+15555555556",
        first_name="Josh",
    )
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555556"
    assert data2["first_name"] == "Josh"
    assert data2["last_name"] == "Doe"


async def test_should_not_partial_update_nonexistent_account(ctx: Context):
    data = await accounts.partial_update(
        ctx,
        account_id=uuid.uuid4(),
        phone_number="+15555555556",
    )
    assert data == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_partial_update_deleted_account(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data3 = await accounts.partial_update(
        ctx,
        account_id=data["account_id"],
        phone_number="+15555555556",
    )
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_delete_account(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"


async def test_should_not_delete_nonexistent_account(ctx: Context):
    data = await accounts.delete(ctx, account_id=uuid.uuid4())
    assert data == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_delete_deleted_account(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="+15555555555",
        password="homeHome123$",
        first_name="John",
        last_name="Doe",
    )
    assert not isinstance(data, ServiceError)
    assert data["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == "+15555555555"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"

    data3 = await accounts.delete(ctx, account_id=data["account_id"])
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND
