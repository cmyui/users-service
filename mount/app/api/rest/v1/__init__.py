from app.api.rest.v1 import accounts
from app.api.rest.v1 import login_attempts
from app.api.rest.v1 import servers
from app.api.rest.v1 import sessions
from fastapi import APIRouter

router = APIRouter()


router.include_router(accounts.router)
router.include_router(login_attempts.router)
router.include_router(servers.router)
router.include_router(sessions.router)
