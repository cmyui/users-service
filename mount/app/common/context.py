from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.services import database


class Context(ABC):
    @property
    @abstractmethod
    def db(self) -> database.ServiceDatabase:
        ...
