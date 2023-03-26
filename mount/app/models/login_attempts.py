from datetime import datetime
from uuid import UUID

from app.models import BaseModel

# input models


class LoginAttemptInput(BaseModel):
    phone_number: str
    ip_address: str
    user_agent: str


# output models


class LoginAttempt(BaseModel):
    login_attempt_id: UUID
    phone_number: str
    ip_address: str
    user_agent: str
    created_at: datetime
