import enum
from typing import List

from graphviz import Digraph

from src.main.core import DatabaseSchemaVisualizer, Table, Relation
from src.main.visualizer import build_table


class VisualizeState(enum.Enum):
    SHOW = 'show'
    LINK = 'link'
    HIDE = 'hide'


class GraphvizDatabaseSchemaVisualizer(DatabaseSchemaVisualizer):

    def __init__(self, tables: List[Table], table_states: dict[str, VisualizeState] = None):
        self.schema = Digraph()
        self.schema.attr("node", shape="plain")
        self.schema.attr(rankdir="TB")
        self.schema.attr(nodesep="1.2")
        self.schema.attr(ranksep="0.8")
        self.schema.attr(TBbalance="max")

        self.tables = tables

        if not table_states:
            table_states = {}
        self.visualize_state = table_states

    def visualize(self):
        self.__create_nodes()
        self.__create_edges_between_all_nodes()

        self.schema.render(filename='erd', format='svg')

    def __create_nodes(self) -> None:
        """
        Создает ноды для таблиц с состоянием SHOW
        """
        for table in self.tables:
            state = self.visualize_state.get(table.name, VisualizeState.SHOW)

            if state == VisualizeState.SHOW:
                self.schema.node(
                    name=table.name,
                    label="<" + build_table(table) + ">"
                )

    def __create_edges_between_all_nodes(self) -> None:
        """
        Создает ребра для отношений каждой из таблиц с состоянием SHOW
        """
        for table in self.tables:
            state = self.visualize_state.get(table.name, VisualizeState.SHOW)

            if state == VisualizeState.SHOW:
                self.__create_edges(table.relations)

    def __create_edges(self, relations: List[Relation]) -> None:
        """
        Создает ребра для отношений между таблицами, только если связанная таблица имеет состояние SHOW или LINK
        """
        for relation in relations:
            related_table_state = self.visualize_state.get(relation.related_table_name, VisualizeState.SHOW)

            if related_table_state == VisualizeState.HIDE:
                continue

            self.schema.edge(
                tail_name=f"{relation.parent_table_name}:{relation.parent_column_name}",
                head_name=f"{relation.related_table_name}:{relation.related_column_name}",
                arrowsize='0.7',
                penwidth='0.7',
                arrowtail='crow',
                dir='back'
            )
