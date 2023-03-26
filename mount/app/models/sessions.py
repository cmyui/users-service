from datetime import datetime

from app.models import BaseModel

# input models


class LoginForm(BaseModel):
    phone_number: str
    password: str


class SessionUpdate(BaseModel):
    expires_at: datetime | None


# output models


class Session(BaseModel):
    session_id: str
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
