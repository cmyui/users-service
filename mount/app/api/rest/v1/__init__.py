from app.api.rest.v1 import accounts
from app.api.rest.v1 import servers
from fastapi import APIRouter

router = APIRouter()


router.include_router(accounts.router)
router.include_router(servers.router)
