import os

from dotenv import load_dotenv

load_dotenv()

# asgi + app
APP_ENV = os.environ["APP_ENV"]
if APP_ENV in ("local", "ci"):
    # TODO: is there a better place for this?
    import email_validator

    email_validator.TEST_ENVIRONMENT = True

APP_COMPONENT = os.environ["APP_COMPONENT"]
APP_HOST = os.environ["APP_HOST"]
APP_PORT = int(os.environ["APP_PORT"])
LOG_LEVEL = int(os.environ["LOG_LEVEL"])

# database
READ_DB_SCHEME = os.environ["READ_DB_SCHEME"]
READ_DB_USER = os.environ["READ_DB_USER"]
READ_DB_PASS = os.environ["READ_DB_PASS"]
READ_DB_HOST = os.environ["READ_DB_HOST"]
READ_DB_PORT = int(os.environ["READ_DB_PORT"])
READ_DB_NAME = os.environ["READ_DB_NAME"]

WRITE_DB_SCHEME = os.environ["WRITE_DB_SCHEME"]
WRITE_DB_USER = os.environ["WRITE_DB_USER"]
WRITE_DB_PASS = os.environ["WRITE_DB_PASS"]
WRITE_DB_HOST = os.environ["WRITE_DB_HOST"]
WRITE_DB_PORT = int(os.environ["WRITE_DB_PORT"])
WRITE_DB_NAME = os.environ["WRITE_DB_NAME"]

# TODO: move these to be per-database settings
DB_CA_CERTIFICATE = os.environ["DB_CA_CERTIFICATE"]
MIN_DB_POOL_SIZE = int(os.environ["MIN_DB_POOL_SIZE"])
MAX_DB_POOL_SIZE = int(os.environ["MAX_DB_POOL_SIZE"])
DB_USE_SSL = os.environ["DB_USE_SSL"].lower() == "true"

REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = int(os.environ["REDIS_PORT"])
REDIS_DB = int(os.environ["REDIS_DB"])
