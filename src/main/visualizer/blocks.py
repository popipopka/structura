from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union


class GraphvizElement(ABC):
    """Базовый класс для всех элементов Graphviz HTML"""

    @abstractmethod
    def __str__(self) -> str:
        pass


@dataclass
class Wrapper(GraphvizElement):
    """Обертка над другими элементами, представленным в строковом виде"""
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass
class LineBreak(GraphvizElement):
    """Перенос строки <BR/>"""

    def __str__(self) -> str:
        return "<BR/>"


@dataclass
class Font(GraphvizElement):
    """Элемент <FONT> с атрибутами"""
    content: Union[str, GraphvizElement, List[GraphvizElement]]
    face: Optional[str] = None
    point_size: Optional[int] = None
    color: Optional[str] = None

    def __str__(self) -> str:
        attrs = []
        if self.face:
            attrs.append(f'face="{self.face}"')
        if self.point_size:
            attrs.append(f'point-size="{self.point_size}"')
        if self.color:
            attrs.append(f'color="{self.color}"')

        attr_str = " ".join(attrs)
        attr_str = f" {attr_str}" if attr_str else ""

        if isinstance(self.content, str):
            content_str = self.content
        elif isinstance(self.content, list):
            content_str = "".join(str(item) for item in self.content)
        else:
            content_str = str(self.content)

        return f"<FONT{attr_str}>{content_str}</FONT>"


@dataclass
class Italic(GraphvizElement):
    """Элемент <I> для курсива"""
    content: Union[str, GraphvizElement, List[GraphvizElement]]

    def __str__(self) -> str:
        if isinstance(self.content, str):
            content_str = self.content
        elif isinstance(self.content, list):
            content_str = "".join(str(item) for item in self.content)
        else:
            content_str = str(self.content)

        return f"<I>{content_str}</I>"


@dataclass
class Bold(GraphvizElement):
    """Элемент <B> для жирного текста"""
    content: Union[str, GraphvizElement, List[GraphvizElement]]

    def __str__(self) -> str:
        if isinstance(self.content, str):
            content_str = self.content
        elif isinstance(self.content, list):
            content_str = "".join(str(item) for item in self.content)
        else:
            content_str = str(self.content)

        return f"<B>{content_str}</B>"


@dataclass
class Cell(GraphvizElement):
    """Элемент <TD> для ячейки таблицы"""
    content: Union[str, GraphvizElement, List[GraphvizElement]]
    port: Optional[str] = None
    align: Optional[str] = None
    bgcolor: Optional[str] = None
    border: Optional[str] = None
    cellborder: Optional[str] = None
    cellpadding: Optional[str] = None
    cellspacing: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None

    def __str__(self) -> str:
        attrs = []
        if self.port:
            attrs.append(f'port="{self.port}"')
        if self.align:
            attrs.append(f'align="{self.align}"')
        if self.bgcolor:
            attrs.append(f'bgcolor="{self.bgcolor}"')
        if self.border:
            attrs.append(f'border="{self.border}"')
        if self.cellborder:
            attrs.append(f'cellborder="{self.cellborder}"')
        if self.cellpadding:
            attrs.append(f'cellpadding="{self.cellpadding}"')
        if self.cellspacing:
            attrs.append(f'cellspacing="{self.cellspacing}"')
        if self.width:
            attrs.append(f'width="{self.width}"')
        if self.height:
            attrs.append(f'height="{self.height}"')

        attr_str = " ".join(attrs)
        attr_str = f" {attr_str}" if attr_str else ""

        if isinstance(self.content, str):
            content_str = self.content
        elif isinstance(self.content, list):
            content_str = "".join(str(item) for item in self.content)
        else:
            content_str = str(self.content)

        return f"<TD{attr_str}>{content_str}</TD>"


@dataclass
class Row(GraphvizElement):
    """Элемент <TR> для строки таблицы"""
    cells: List[Cell]

    def __str__(self) -> str:
        cells_str = "".join(str(cell) for cell in self.cells)
        return f"<TR>{cells_str}</TR>"


@dataclass
class Table(GraphvizElement):
    """Элемент <TABLE> для таблицы"""
    rows: List[Row]
    border: Optional[str] = None
    cellborder: Optional[str] = None
    cellspacing: Optional[str] = None
    cellpadding: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None
    bgcolor: Optional[str] = None
    color: Optional[str] = None
    port: Optional[str] = None
    sides: Optional[str] = None
    title: Optional[str] = None
    tooltip: Optional[str] = None
    href: Optional[str] = None
    target: Optional[str] = None
    id: Optional[str] = None
    class_name: Optional[str] = None
    style: Optional[str] = None

    def __str__(self) -> str:
        attrs = []
        if self.border:
            attrs.append(f'border="{self.border}"')
        if self.cellborder:
            attrs.append(f'cellborder="{self.cellborder}"')
        if self.cellspacing:
            attrs.append(f'cellspacing="{self.cellspacing}"')
        if self.cellpadding:
            attrs.append(f'cellpadding="{self.cellpadding}"')
        if self.width:
            attrs.append(f'width="{self.width}"')
        if self.height:
            attrs.append(f'height="{self.height}"')
        if self.bgcolor:
            attrs.append(f'bgcolor="{self.bgcolor}"')
        if self.color:
            attrs.append(f'color="{self.color}"')
        if self.port:
            attrs.append(f'port="{self.port}"')
        if self.sides:
            attrs.append(f'sides="{self.sides}"')
        if self.title:
            attrs.append(f'title="{self.title}"')
        if self.tooltip:
            attrs.append(f'tooltip="{self.tooltip}"')
        if self.href:
            attrs.append(f'href="{self.href}"')
        if self.target:
            attrs.append(f'target="{self.target}"')
        if self.id:
            attrs.append(f'id="{self.id}"')
        if self.class_name:
            attrs.append(f'class="{self.class_name}"')
        if self.style:
            attrs.append(f'style="{self.style}"')

        attr_str = " ".join(attrs)
        attr_str = f" {attr_str}" if attr_str else ""

        rows_str = "".join(str(row) for row in self.rows)
        return f"<TABLE{attr_str}>{rows_str}</TABLE>"


def join_blocks(delimiter: str, *blocks: Union[GraphvizElement, List[GraphvizElement]]) -> Wrapper:
    """Объединяет несколько текстовых блоков через пробел"""
    elements = []
    for block in blocks:
        if isinstance(block, list):
            elements.extend(block)
        else:
            elements.append(block)
    return Wrapper(delimiter.join(str(el) for el in elements))
