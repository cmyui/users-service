from enum import Enum


class ServiceError(str, Enum):
    SERVERS_CREATION_FAILED = "servers.creation_failed"
    SERVERS_NAME_ALREADY_EXISTS = "servers.name_already_exists"
    SERVERS_NOT_FOUND = "servers.not_found"
