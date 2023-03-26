import uuid

from app.common import formatters
from app.common.context import Context
from app.common.errors import ServiceError
from app.services import accounts
from testing import sample_data


async def test_should_create_account(ctx: Context):
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


async def test_should_not_create_account_with_invalid_phone_number(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number="15555555555",
        password=sample_data.fake_password(),
        first_name=sample_data.fake_first_name(),
        last_name=sample_data.fake_last_name(),
    )
    assert data == ServiceError.ACCOUNTS_PHONE_NUMBER_INVALID


async def test_should_not_create_account_with_invalid_password(ctx: Context):
    data = await accounts.create(
        ctx,
        phone_number=sample_data.fake_phone_number(),
        password="abc",
        first_name=sample_data.fake_first_name(),
        last_name=sample_data.fake_last_name(),
    )
    assert data == ServiceError.ACCOUNTS_PASSWORD_INVALID


async def test_should_not_create_account_with_preexisting_phone_number(ctx: Context):
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

    data2 = await accounts.create(
        ctx,
        phone_number=phone_number,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    assert data2 == ServiceError.ACCOUNTS_PHONE_NUMBER_EXISTS


async def test_should_fetch_one_account_by_id(ctx: Context):
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

    data2 = await accounts.fetch_one(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name


async def test_should_fetch_one_account_by_phone_number(ctx: Context):
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

    data2 = await accounts.fetch_one(ctx, phone_number=phone_number)
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name


async def test_should_not_fetch_one_nonexistent_account(ctx: Context):
    data = await accounts.fetch_one(ctx, account_id=uuid.uuid4())
    assert data == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_fetch_one_deleted_account_by_id(ctx: Context):
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

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name

    data3 = await accounts.fetch_one(ctx, account_id=data["account_id"])
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_fetch_one_deleted_account_by_phone_number(ctx: Context):
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

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name

    data3 = await accounts.fetch_one(ctx, phone_number=data["phone_number"])
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_fetch_all_accounts(ctx: Context):
    expected = []
    for _ in range(3):
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

        expected.append(data)

    data2 = await accounts.fetch_many(ctx)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 3

    for account_data, expected_data in zip(data2, expected):
        assert account_data["phone_number"] == expected_data["phone_number"]
        assert "password" not in account_data
        assert account_data["first_name"] == expected_data["first_name"]
        assert account_data["last_name"] == expected_data["last_name"]


async def test_should_fetch_one_page_of_accounts(ctx: Context):
    expected = []
    for _ in range(3):
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

    data2 = await accounts.fetch_many(ctx, page=1, page_size=2)
    assert not isinstance(data2, ServiceError)
    assert len(data2) == 2

    for account_data, expected_data in zip(data2, expected):
        assert account_data["phone_number"] == expected_data["phone_number"]
        assert "password" not in account_data
        assert account_data["first_name"] == expected_data["first_name"]
        assert account_data["last_name"] == expected_data["last_name"]


async def test_should_partial_update_account(ctx: Context):
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

    phone_number = sample_data.fake_phone_number()
    first_name = sample_data.fake_first_name()

    data2 = await accounts.partial_update(
        ctx,
        account_id=data["account_id"],
        phone_number=phone_number,
        first_name=first_name,
    )
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name


async def test_should_not_partial_update_nonexistent_account(ctx: Context):
    data = await accounts.partial_update(
        ctx,
        account_id=uuid.uuid4(),
        phone_number=sample_data.fake_phone_number(),
    )
    assert data == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_partial_update_deleted_account(ctx: Context):
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

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name

    data3 = await accounts.partial_update(
        ctx,
        account_id=data["account_id"],
        phone_number=sample_data.fake_phone_number(),
    )
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_delete_account(ctx: Context):
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

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name


async def test_should_not_delete_nonexistent_account(ctx: Context):
    data = await accounts.delete(ctx, account_id=uuid.uuid4())
    assert data == ServiceError.ACCOUNTS_NOT_FOUND


async def test_should_not_delete_deleted_account(ctx: Context):
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

    data2 = await accounts.delete(ctx, account_id=data["account_id"])
    assert not isinstance(data2, ServiceError)
    assert data2["phone_number"] == formatters.phone_number(phone_number)
    assert "password" not in data2
    assert data2["first_name"] == first_name
    assert data2["last_name"] == last_name

    data3 = await accounts.delete(ctx, account_id=data["account_id"])
    assert data3 == ServiceError.ACCOUNTS_NOT_FOUND
