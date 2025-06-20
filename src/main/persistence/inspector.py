from typing import List

from sqlalchemy import inspect
from sqlalchemy.engine.interfaces import ReflectedColumn, ReflectedForeignKeyConstraint

from src.main.core import DatabaseSchemaOutputPort, Table, Column, Relation
from src.main.persistence import Connection


class DatabaseSchemaInspectorAdapter(DatabaseSchemaOutputPort):
    def __init__(self, connection: Connection):
        self.inspector = inspect(connection.engine)

    def get_tables(self, schema: str | None = "public") -> List[Table]:
        table_names = self.__get_table_names(schema)

        tables = []
        for table_name in table_names:
            columns = self.__get_all_columns(table_name)
            relations = self.__get_foreign_keys(table_name)

            tables.append(Table(
                name=table_name,
                columns=columns,
                relations=relations
            ))

        return tables

    def __get_table_names(self, schema: str) -> List[str]:
        return self.inspector.get_table_names(schema)

    def __get_all_columns(self, table_name: str) -> List[Column]:
        reflected_columns = self.inspector.get_columns(table_name)
        pk_columns = self.__get_primary_key_columns(table_name)
        fk_columns = self.__get_foreign_key_columns(table_name)
        unique_columns = self.__get_unique_columns(table_name)
        
        return [map_reflected_column_to_column(e, pk_columns, fk_columns, unique_columns) for e in reflected_columns]

    def __get_primary_key_columns(self, table_name: str) -> List[str]:
        pk_constraint = self.inspector.get_pk_constraint(table_name)
        return pk_constraint.get('constrained_columns', [])

    def __get_foreign_key_columns(self, table_name: str) -> List[str]:
        foreign_keys = self.inspector.get_foreign_keys(table_name)
        fk_columns = []
        for fk in foreign_keys:
            fk_columns.extend(fk.get('constrained_columns', []))
        return fk_columns

    def __get_unique_columns(self, table_name: str) -> List[str]:
        indexes = self.inspector.get_indexes(table_name)
        unique_columns = []
        for index in indexes:
            if index.get('unique', False):
                unique_columns.extend(index.get('column_names', []))
        return unique_columns

    def __get_foreign_keys(self, table_name: str) -> List[Relation]:
        foreign_keys = self.inspector.get_foreign_keys(table_name)
        return [map_foreign_key_to_relation(table_name, e) for e in foreign_keys]


def map_reflected_column_to_column(reflected_column: ReflectedColumn,
                                 pk_columns: List[str], fk_columns: List[str], unique_columns: List[str]) -> Column:
    column_name = reflected_column.get('name')
    
    return Column(
        name=column_name,
        type=str(reflected_column.get('type')),
        is_primary_key=column_name in pk_columns,
        is_foreign_key=column_name in fk_columns,
        is_unique=column_name in unique_columns,
        is_nullable=reflected_column.get('nullable', True)
    )


def map_foreign_key_to_relation(table_name: str, foreign_key: ReflectedForeignKeyConstraint) -> Relation:
    parent_column_name = foreign_key.get('constrained_columns')[0]
    related_table_name = foreign_key.get('referred_table')
    related_column_name = foreign_key.get('referred_columns')[0]

    return Relation(
        parent_table_name=table_name,
        parent_column_name=parent_column_name,
        related_table_name=related_table_name,
        related_column_name=related_column_name
    )