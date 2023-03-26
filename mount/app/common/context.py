from abc import ABC
from abc import abstractmethod

import redis.asyncio as aioredis
from app.adapters import database


class Context(ABC):
    @property
    @abstractmethod
    def db(self) -> database.ServiceDatabase:
        ...

    @property
    @abstractmethod
    def redis(self) -> aioredis.Redis:
        ...
