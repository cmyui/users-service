from abc import ABC
from abc import abstractmethod

from app.adapters import database


class Context(ABC):
    @property
    @abstractmethod
    def db(self) -> database.ServiceDatabase:
        ...
