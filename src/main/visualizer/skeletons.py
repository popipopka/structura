from typing import List

from src.main.core import Column, Table


def fill_and_get_table_html_skeleton(table: Table) -> str:
    return f'''<
    <table border='0' cellborder='1' cellspacing='0'>
        <tr>
            <td bgcolor='lightblue'><b>{table.name}</b></td>
        </tr>
        
        {fill_and_get_all_column_html_skeletons(table.columns)}
    </table>
    >'''


def fill_and_get_all_column_html_skeletons(columns: List[Column]) -> str:
    return ''.join([fill_and_get_column_html_skeleton(e) for e in columns])


def fill_and_get_column_html_skeleton(column: Column) -> str:
    return f'''
    <tr>
        <td port='{column.name}'>{column.name}</td>
    </tr>
    '''
