from datetime import datetime
from uuid import UUID

from app.models import BaseModel
from app.models import Status

# input models


class SignupForm(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str


class AccountUpdate(BaseModel):
    username: str | None
    first_name: str | None
    last_name: str | None


# output models


class Account(BaseModel):
    account_id: UUID
    username: str
    first_name: str
    last_name: str
    status: Status
    created_at: datetime
    updated_at: datetime
