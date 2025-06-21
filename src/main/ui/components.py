import flet as ft

class DatabaseCard(ft.Container):
    def __init__(self, name, dialect, on_select):
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
        self._on_select = on_select
        self._dialect = dialect

    def _on_click(self, e):
        if self._on_select:
            self._on_select(self._dialect)


class ConnectionHistoryCard(ft.Container):
    def __init__(self, history, on_delete, on_select, on_edit):
        dialect = history.get('dialect')
        dialect_name = dialect.value.upper()
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
        self._on_select = on_select

    def _on_click(self, e):
        if self._on_select:
            self._on_select(self.content.controls[0].value)