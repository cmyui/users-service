from enum import Enum


class ServiceError(str, Enum):
    ACCOUNTS_CREATION_FAILED = "accounts.creation_failed"
    ACCOUNTS_DELETION_FAILED = "accounts.deletion_failed"
    ACCOUNTS_NOT_FOUND = "accounts.not_found"
    ACCOUNTS_USERNAME_INVALID = "accounts.username_invalid"
    ACCOUNTS_PASSWORD_INVALID = "accounts.password_invalid"
    ACCOUNTS_COUNTRY_INVALID = "accounts.country_invalid"
    ACCOUNTS_USERNAME_EXISTS = "accounts.username_exists"

    # security to hide the fact that the username exists
    CREDENTIALS_INCORRECT = "credentials.incorrect"

    SESSIONS_CREATION_FAILED = "sessions.creation_failed"
    SESSIONS_DELETION_FAILED = "sessions.deletion_failed"
    SESSIONS_NOT_FOUND = "sessions.not_found"
    SESSIONS_USERNAME_INVALID = "sessions.username_invalid"
    SESSIONS_PASSWORD_INVALID = "sessions.password_invalid"
    SESSIONS_PASSWORD_INCORRECT = "sessions.password_incorrect"

    LOGIN_ATTEMPTS_NOT_FOUND = "login_attempts.attempt_not_found"
    LOGIN_ATTEMPTS_CREATION_FAILED = "login_attempts.creation_failed"
    LOGIN_ATTEMPTS_DELETION_FAILED = "login_attempts.deletion_failed"
    LOGIN_ATTEMPTS_USERNAME_INVALID = "login_attempts.username_invalid"
