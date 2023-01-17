from __future__ import annotations

from enum import Enum


class ServiceError(str, Enum):
    SERVERS_CANNOT_CREATE = "servers.cannot_create"
    SERVERS_NAME_ALREADY_EXISTS = "servers.name_already_exists"
    SERVERS_NOT_FOUND = "servers.not_found"
