from abc import ABC, abstractmethod
from typing import List

from src.main.core import Table


class DatabaseSchemaOutputPort(ABC):
    @abstractmethod
    def get_tables(self, schema: str | None = "public") -> List[Table]:
        pass