from typing import List

from sqlalchemy import inspect
from sqlalchemy.engine.interfaces import ReflectedColumn, ReflectedForeignKeyConstraint

from src.main.core import DatabaseSchemaOutputPort, Table, Column, Relation
from src.main.persistence import Connection, DatabaseURL, Dialect


class DatabaseSchemaInspectorAdapter(DatabaseSchemaOutputPort):
    def __init__(self, connection: Connection):
        self.inspector = inspect(connection.engine)

    def get_tables(self, schema: str | None = "public") -> List[Table]:
        table_names = self.__get_table_names(schema)

        tables = []
        for table_name in table_names:
            columns = self.__get_columns(table_name)
            relations = self.__get_foreign_keys(table_name)

            tables.append(Table(
                name=table_name,
                columns=columns,
                relations=relations
            ))

        return tables

    def __get_table_names(self, schema: str) -> List[str]:
        return self.inspector.get_table_names(schema)

    def __get_columns(self, table_name: str) -> List[Column]:
        reflected_columns = self.inspector.get_columns(table_name)
        return [map_reflected_column_to_column(e) for e in reflected_columns]

    def __get_foreign_keys(self, table_name: str) -> List[Relation]:
        foreign_keys = self.inspector.get_foreign_keys(table_name)
        return [map_foreign_key_to_relation(table_name, e) for e in foreign_keys]


def map_reflected_column_to_column(reflected_column: ReflectedColumn) -> Column:
    return Column(reflected_column.get('name'))


def map_foreign_key_to_relation(table_name: str, foreign_key: ReflectedForeignKeyConstraint) -> Relation:
    return Relation(
        parent_table_name=table_name,
        parent_column_name=foreign_key.get('constrained_columns')[0],
        related_table_name=foreign_key.get('referred_table'),
        related_column_name=foreign_key.get('referred_columns')[0]
    )