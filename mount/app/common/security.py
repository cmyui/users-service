from typing import Literal

import argon2

ph = argon2.PasswordHasher()


def hash_password(password: str | bytes) -> str:
    return ph.hash(password)


def verify_password(
    hashed_password: str | bytes,
    password: str | bytes,
) -> bool:
    try:
        ph.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False
    else:
        return True
