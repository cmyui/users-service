import random

from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)


def fake_phone_number() -> str:
    # XXX: many numbers returned from faker's phone number generator
    # do not pass the phonenumbers.parse() check, so we implement this
    formats = [
        "({}{}{}) {}{}{}-{}{}{}{}",
        "{}{}{}{}{}{}{}{}{}{}",
        "({}{}{})-{}{}{}-{}{}{}{}",
        "{}{}{}.{}{}{}.{}{}{}{}",
    ]

    ten_numbers = [random.randint(0, 9) for _ in range(10)]
    phone_number = random.choice(formats).format(*ten_numbers)

    # TODO: add more country codes
    phone_number = "+1" + phone_number

    return phone_number


def fake_email() -> str:
    return fake.email()


def fake_first_name() -> str:
    return fake.first_name()


def fake_last_name() -> str:
    return fake.last_name()


def fake_ipv4_address() -> str:
    return fake.ipv4()


def fake_user_agent() -> str:
    return fake.user_agent()


def fake_password() -> str:
    return fake.password()
