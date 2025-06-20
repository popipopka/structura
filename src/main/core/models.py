from typing import List
from dataclasses import dataclass


@dataclass
class Column:
    name: str
    type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_unique: bool = False
    is_nullable: bool = True


@dataclass
class Relation:
    parent_table_name: str
    parent_column_name: str
    related_table_name: str
    related_column_name: str


@dataclass
class Table:
    name: str
    columns: List[Column]
    relations: List[Relation]
