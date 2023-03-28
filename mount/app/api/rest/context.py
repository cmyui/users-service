import redis.asyncio as aioredis
from app.adapters import database
from app.common.context import Context
from fastapi import Request


class RequestContext(Context):
    def __init__(self, request: Request) -> None:
        self.request = request

    @property
    def db(self) -> database.ServiceDatabase:
        return self.request.state.db

    @property
    def redis(self) -> aioredis.Redis:
        return self.request.state.redis
