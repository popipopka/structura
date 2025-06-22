from typing import Callable, Dict, Any

import flet as ft

from src.main.persistence import Dialect
from src.main.visualizer import VisualizeState


class DatabaseCard(ft.Container):
    def __init__(self, name: str, dialect: Dialect, on_select: Callable[[Dialect], None]) -> None:
        super().__init__(
            content=ft.Column(
                [ft.Text(name, size=15, weight=ft.FontWeight.BOLD), ],
                alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=15,
            alignment=ft.alignment.center,
            width=160,
            height=80,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=12,
            bgcolor=ft.Colors.SURFACE,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.SHADOW, offset=ft.Offset(0, 2)),
            ink=True,
            on_click=self._on_click,
        )
        self._on_select: Callable[[Dialect], None] = on_select
        self._dialect: Dialect = dialect

    def _on_click(self, e: ft.ControlEvent) -> None:
        if self._on_select:
            self._on_select(self._dialect)


class ConnectionHistoryCard(ft.Container):
    def __init__(
            self,
            history: Dict[str, Any],
            on_delete: Callable[[str], None],
            on_select: Callable[[Dict[str, Any]], None],
            on_edit: Callable[[Dict[str, Any]], None]
    ) -> None:
        dialect: Dialect = history.get('dialect')
        dialect_name: str = dialect.value.upper()
        super().__init__(
            content=ft.Row([
                ft.Column(
                    [
                        ft.Text(dialect_name, size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(history['database'], size=16, color=ft.Colors.BLUE),
                        ft.Text(f"{history['host']}:{history['port']}", size=12, color=ft.Colors.GREY),
                        ft.Text(history['user'], size=12, color=ft.Colors.GREY),
                    ],
                    spacing=4,
                    expand=True
                ),

                ft.Column(
                    [
                        ft.IconButton(
                            ft.Icons.EDIT,
                            icon_color=ft.Colors.PRIMARY,
                            icon_size=28,
                            tooltip="Изменить",
                            on_click=lambda e: on_edit(history)
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            icon_size=28,
                            tooltip="Удалить",
                            on_click=lambda e: on_delete(history.get('uuid'))
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=16,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=12,
            bgcolor=ft.Colors.SURFACE,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.SHADOW, offset=ft.Offset(0, 2)),
            ink=True,
            on_click=lambda e: on_select(history),
        )
        self._on_select: Callable[[Dict[str, Any]], None] = on_select

    def _on_click(self, e: ft.ControlEvent) -> None:
        if self._on_select:
            self._on_select(self.content.controls[0].value)


class TableVisibilitySelector(ft.Row):
    def __init__(
            self,
            table_name: str,
            selected_value: VisualizeState,
            on_change: Callable[[ft.ControlEvent], None]
    ) -> None:
        super().__init__(
            controls=[
                ft.Text(table_name, expand=True),
                ft.RadioGroup(
                    content=ft.Row(
                        [
                            ft.Radio(value=VisualizeState.SHOW.value),
                            ft.Radio(value=VisualizeState.LINK.value),
                            ft.Radio(value=VisualizeState.HIDE.value),
                        ],
                        spacing=6,
                    ),
                    value=selected_value.value,
                    on_change=on_change,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=8,
            expand=True
        )
