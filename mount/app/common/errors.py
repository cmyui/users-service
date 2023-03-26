from enum import Enum


class ServiceError(str, Enum):
    SERVERS_CREATION_FAILED = "servers.creation_failed"
    SERVERS_NAME_ALREADY_EXISTS = "servers.name_already_exists"
    SERVERS_NOT_FOUND = "servers.not_found"

    ACCOUNTS_CREATION_FAILED = "accounts.creation_failed"
    ACCOUNTS_DELETION_FAILED = "accounts.deletion_failed"
    ACCOUNTS_NOT_FOUND = "accounts.not_found"
    ACCOUNTS_USERNAME_INVALID = "accounts.username_invalid"
    ACCOUNTS_PASSWORD_INVALID = "accounts.password_invalid"
    ACCOUNTS_PHONE_NUMBER_INVALID = "accounts.phone_number_invalid"
    ACCOUNTS_COUNTRY_INVALID = "accounts.country_invalid"
    ACCOUNTS_PHONE_NUMBER_EXISTS = "accounts.phone_number_exists"
    ACCOUNTS_USERNAME_EXISTS = "accounts.username_exists"

    CREDENTIALS_CREATION_FAILED = "credentials.creation_failed"
    CREDENTIALS_DELETION_FAILED = "credentials.deletion_failed"
    CREDENTIALS_NOT_FOUND = "credentials.incorrect_credentials"
    CREDENTIALS_INCORRECT = "credentials.incorrect_credentials"

    SESSIONS_CREATION_FAILED = "sessions.creation_failed"
    SESSIONS_DELETION_FAILED = "sessions.deletion_failed"
    SESSIONS_NOT_FOUND = "sessions.not_found"

    LOGIN_ATTEMPTS_NOT_FOUND = "login_attempts.attempt_not_found"
    LOGIN_ATTEMPTS_CREATION_FAILED = "login_attempts.creation_failed"
    LOGIN_ATTEMPTS_DELETION_FAILED = "login_attempts.deletion_failed"
    LOGIN_ATTEMPTS_PHONE_NUMBER_INVALID = "login_attempts.phone_number_invalid"
