from datetime import datetime
from uuid import UUID

from app.models import BaseModel

# input models


# output models


class LoginAttempt(BaseModel):
    login_attempt_id: UUID
    phone_number: str
    ip_address: str
    user_agent: str
    # TODO: should we store result? (success, failure)
    created_at: datetime
