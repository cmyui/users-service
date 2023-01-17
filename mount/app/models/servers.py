from datetime import datetime

from app.models import BaseModel
from app.models import Status

# input models


class ServerInput(BaseModel):
    server_name: str
    hourly_request_limit: int


class ServerUpdate(BaseModel):
    server_name: str | None
    hourly_request_limit: int | None


# output models
class Server(BaseModel):
    server_id: int
    server_name: str
    hourly_request_limit: int
    status: Status
    created_at: datetime
    updated_at: datetime
