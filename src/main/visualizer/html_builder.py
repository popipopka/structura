from src.main.core import Column, Table as TableModel
from src.main.visualizer.blocks import *


def build_table(table: TableModel) -> str:
    table_rows = [build_table_header_row(table.name)]

    for column in table.columns:
        table_rows.append(build_table_column_row(column))

    table_element = Table(
        rows=table_rows,
        border="0",
        cellborder="1",
        cellspacing="0"
    )

    return str(table_element)


def build_table_header_row(table_name: str) -> Row:
    """Создает строку заголовка таблицы"""
    return Row(cells=[
        Cell(
            content=Bold(Font(table_name, face="Arial", point_size=9)),
            bgcolor="lightblue"
        )
    ])


def build_table_column_row(column: Column) -> Row:
    key_info = ""
    if column.is_primary_key:
        key_info = "PK"
    elif column.is_foreign_key:
        key_info = "FK"
    elif column.is_unique:
        key_info = "UQ"

    color = "gray"
    if column.is_primary_key:
        color = "blue"
    elif column.is_foreign_key:
        color = "green"
    elif column.is_unique:
        color = "purple"

    nullable_info = "NULL" if column.is_nullable else ""

    content = [
        Bold(Font(column.name, face="Arial", point_size=9)),
        LineBreak()
    ]

    if key_info:
        content.append(
            Bold(Font(key_info, face="Arial", point_size=7, color=color))
        )

    content.append(
        Italic(Font(column.type, face="Arial", point_size=7, color="gray"))
    )

    if nullable_info:
        content.append(
            Font(nullable_info, face="Arial", point_size=7, color="gray")
        )


    return Row(cells=[
        Cell(
            content=join_blocks(" ", content),
            port=column.name
        )
    ])
