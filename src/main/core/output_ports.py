from abc import ABC, abstractmethod
from typing import List

from src.main.core import Table


class DatabaseSchemaInspector(ABC):
    @abstractmethod
    def get_tables(self) -> List[Table]:
        pass

class DatabaseSchemaVisualizer(ABC):
    @abstractmethod
    def visualize(self):
        pass