from typing import List

from graphviz import Digraph

from src.main.core import DatabaseSchemaVisualizer, Table, Relation
from src.main.visualizer import fill_and_get_table_html_skeleton


class GraphvizDatabaseSchemaVisualizer(DatabaseSchemaVisualizer):

    def __init__(self, tables: List[Table]):
        self.schema = Digraph()
        self.schema.attr("node", shape="plain")
        self.schema.attr(rankdir="LR")

        self.tables = tables

    def visualize(self):
        self.__create_nodes()
        self.__create_edges_between_all_nodes()

        self.schema.render(filename='erd', format='png')

    def __create_nodes(self) -> None:
        for table in self.tables:
            self.schema.node(
                name=table.name,
                label=fill_and_get_table_html_skeleton(table)
            )

    def __create_edges_between_all_nodes(self) -> None:
        for table in self.tables:
            self.__create_edges(table.relations)

    def __create_edges(self, relations: List[Relation]) -> None:
        for relation in relations:
            self.schema.edge(
                tail_name=f"{relation.parent_table_name}:{relation.parent_column_name}",
                head_name=f"{relation.related_table_name}:{relation.related_column_name}",
            )
