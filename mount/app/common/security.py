from typing import Literal

from argon2 import PasswordHasher

ph = PasswordHasher()


def hash_password(password: str | bytes) -> str:
    return ph.hash(password)


def verify_password(
    hashed_password: str | bytes,
    password: str | bytes,
) -> Literal[True]:
    return ph.verify(hashed_password, password)
