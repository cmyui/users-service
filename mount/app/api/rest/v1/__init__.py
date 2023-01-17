from __future__ import annotations

from app.api.rest.v1 import servers
from fastapi import APIRouter

router = APIRouter()


router.include_router(servers.router)
