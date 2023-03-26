from datetime import datetime

from app.models import BaseModel
from app.models import Status

# input models


class SignupForm(BaseModel):
    phone_number: str
    password: str
    first_name: str
    last_name: str


class AccountUpdate(BaseModel):
    phone_number: str | None
    first_name: str | None
    last_name: str | None


# output models


class Account(BaseModel):
    id: int
    phone_number: str
    first_name: str
    last_name: str
    status: Status
    created_at: datetime
    updated_at: datetime
