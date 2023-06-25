from datetime import datetime
from uuid import UUID

from app.models import BaseModel

# input models


class LoginForm(BaseModel):
    username: str
    password: str


class SessionUpdate(BaseModel):
    expires_at: datetime | None


# output models


class Session(BaseModel):
    session_id: UUID
    account_id: UUID
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
