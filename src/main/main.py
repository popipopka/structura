import json
import os
import uuid
import re

import flet as ft

from src.main.persistence import DatabaseURL, Dialect, Connection
from src.main.persistence.inspector import DatabaseSchemaInspectorAdapter
from src.main.visualizer.visualizer import GraphvizDatabaseSchemaVisualizer


# --- UI Components ---
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
        self._hovered = False

    def _on_click(self, e):
        if self._on_select:
            self._on_select(self._dialect)


class ConnectionHistoryCard(ft.Container):
    def __init__(self, history, on_delete, on_select):
        # Get dialect name for display
        dialect = history.get('dialect', Dialect.POSTGRESQL)
        if hasattr(dialect, 'name'):
            dialect_name = dialect.name
        elif hasattr(dialect, 'value'):
            dialect_name = dialect.value.upper()
        else:
            dialect_name = 'Unknown'  # fallback

        super().__init__(
            content=ft.Column([
                ft.Row(
                    [
                        ft.Text(dialect_name, size=14, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            icon_size=28,
                            tooltip="Удалить",
                            on_click=lambda e: on_delete(history.get('uuid'))
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Text(f"{history['host']}:{history['port']}", size=14, color=ft.Colors.GREY),
                ft.Text(history['database'], size=15, color=ft.Colors.BLUE),
            ], spacing=3),
            padding=16,
            width=200,
            height=100,
            border=ft.border.all(2, ft.Colors.OUTLINE),
            border_radius=12,
            bgcolor=ft.Colors.SURFACE,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.SHADOW, offset=ft.Offset(0, 2)),
            ink=True,
            on_click=lambda e: on_select(history),
        )
        self._on_select = on_select
        self._hovered = False

    def _on_click(self, e):
        if self._on_select:
            self._on_select(self.content.controls[2].value)  # Передаем базу данных (или можно всю history)


# --- Storage and Logic ---
def save_connection_history(history):
    serializable_history = []

    for h in history:
        h_copy = h.copy()
        # Add UUID if not present
        if 'uuid' not in h_copy:
            h_copy['uuid'] = str(uuid.uuid4())
        if 'dialect' in h_copy:
            h_copy['dialect'] = h_copy['dialect'].value
        serializable_history.append(h_copy)

    with open("connections.json", "w") as f:
        json.dump(serializable_history, f)


def load_connection_history():
    if not os.path.exists("connections.json"):
        return []
    with open("connections.json", "r") as f:
        history = json.load(f)

    # Конвертируем строки обратно в Dialect и добавляем UUID если отсутствует
    for h in history:
        if 'dialect' in h:
            h['dialect'] = Dialect.from_value(h['dialect'])
        # Add UUID if not present (for backward compatibility)
        if 'uuid' not in h:
            h['uuid'] = str(uuid.uuid4())

    return history


def generate_erd_svg(db_url):
    conn = Connection(db_url)
    inspector = DatabaseSchemaInspectorAdapter(conn)
    visualizer = GraphvizDatabaseSchemaVisualizer(inspector.get_tables())
    visualizer.visualize()  # сохраняет erd.svg
    with open("./erd.svg", "r") as f:
        return f.read()


def get_svg_size(svg_text):
    match = re.search(r'<svg[^>]*width="([\d.]+)[a-zA-Z]*"[^>]*height="([\d.]+)[a-zA-Z]*"', svg_text)

    width = float(match.group(1))
    height = float(match.group(2))

    return width, height


def main(page: ft.Page):
    page.title = "Structura"
    page.window_width = 900
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK

    # State
    connection_history = load_connection_history()
    current_db_url = None
    svg_data = None

    def go_to_screen(screen):
        page.views.clear()
        page.views.append(screen)
        page.update()

    # --- Screen 1: DB Choice ---
    def db_choice_screen():
        # --- Database Cards ---
        db_cards = [
            DatabaseCard(
                name=Dialect.POSTGRESQL.value.upper(),
                dialect=Dialect.POSTGRESQL,
                on_select=lambda dialect: go_to_screen(connection_input_screen(dialect))
            )
        ]
        db_cards_row = ft.Row(db_cards, alignment=ft.MainAxisAlignment.CENTER, spacing=24)

        # --- Connection History Cards ---
        def delete_history(connection_uuid):
            # Find and remove connection by UUID
            connection_history[:] = [h for h in connection_history if h.get('uuid') != connection_uuid]
            save_connection_history(connection_history)
            go_to_screen(db_choice_screen())

        def quick_connect(h):
            nonlocal current_db_url
            # Используем диалект из истории или по умолчанию PostgreSQL
            dialect: Dialect = h.get('dialect', Dialect.POSTGRESQL)
            current_db_url = DatabaseURL(
                dialect, h['user'], h['password'], h['host'], h['port'], h['database']
            )
            go_to_screen(erd_screen())

        history_cards = [
            ConnectionHistoryCard(
                history=h,
                on_delete=delete_history,
                on_select=quick_connect
            ) for h in connection_history
        ]

        history_grid = ft.GridView(
            controls=history_cards,
            max_extent=220,
            child_aspect_ratio=1.6,
            spacing=16,
            run_spacing=16,
            expand=True,
        ) if history_cards else ft.Text("Нет прошлых подключений", size=16, color=ft.Colors.RED)

        # --- Layout ---
        return ft.View(
            "/db_choice",
            [
                ft.Container(
                    ft.Text("Выберите базу данных:", size=24, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=20, bottom=5)
                ),
                db_cards_row,
                ft.Container(
                    ft.Divider(height=2, thickness=2, color=ft.Colors.GREY_300),
                    padding=ft.padding.symmetric(vertical=20),
                    expand=True
                ),
                ft.Container(
                    ft.Text("Прошлые подключения:", size=18, weight=ft.FontWeight.BOLD),
                    alignment=ft.alignment.center_left,
                    padding=ft.padding.only(left=40, bottom=10)
                ),
                ft.Container(
                    history_grid,
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(left=40, right=40, bottom=10),
                    expand=True
                )
            ]
        )

    # --- Screen 2: Connection Input ---
    def connection_input_screen(dialect):
        card_width = 400
        field_height = 44
        host = ft.TextField(label="Host", value="localhost", height=field_height, width=card_width * 0.65)
        port = ft.TextField(label="Port", value="5432", height=field_height, expand=True)
        user = ft.TextField(label="User", value="postgres", height=field_height, width=card_width)
        password = ft.TextField(label="Password", password=True, can_reveal_password=True, height=field_height,
                                width=card_width)
        database = ft.TextField(label="Database", height=field_height, width=card_width)
        error_text = ft.Text("", color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)

        def on_accept(e):
            if not all([host.value, port.value, user.value, password.value, database.value]):
                error_text.value = "Все поля должны быть заполнены!"
                page.update()
                return
            try:
                db_url = DatabaseURL(dialect, user.value, password.value, host.value, int(port.value),
                                     database.value)
                # Проверка подключения
                conn = Connection(db_url)
                conn.get_engine().connect().close()

                # Сохраняем в историю только после успешного подключения
                h = dict(
                    uuid=str(uuid.uuid4()),
                    user=user.value,
                    password=password.value,
                    host=host.value,
                    port=int(port.value),
                    database=database.value,
                    dialect=dialect
                )
                if h not in connection_history:
                    connection_history.append(h)
                    save_connection_history(connection_history)

                nonlocal current_db_url
                current_db_url = db_url
                go_to_screen(erd_screen())
            except Exception as ex:
                error_text.value = f"Ошибка подключения: {ex}"
                page.update()

        return ft.View(
            "/connection_input",
            [
                ft.Container(
                    content=ft.Container(
                        ft.Column([
                            ft.Text("Введите данные для подключения", size=20, weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER),
                            ft.Row([
                                host,
                                port
                            ], spacing=8, alignment=ft.MainAxisAlignment.CENTER),
                            user,
                            password,
                            database,
                            error_text,
                            ft.Row([
                                ft.OutlinedButton("Назад", on_click=lambda e: go_to_screen(db_choice_screen()),
                                                  expand=True, height=field_height),
                                ft.FilledButton("Принять", on_click=on_accept, expand=True, height=field_height),
                            ], spacing=8),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12),
                        padding=28,
                        width=card_width,
                        height=420,
                        alignment=ft.alignment.center,
                    ),
                    # elevation=6,
                    # color=ft.Colors.SURFACE,
                    # shadow_color=ft.Colors.SHADOW,
                    # shape=ft.RoundedRectangleBorder(radius=24),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )

    # --- Screen 3: ERD SVG ---
    def erd_screen():
        nonlocal svg_data
        svg_data = generate_erd_svg(current_db_url)
        svg_view = ft.Image(src_base64=None, src=None)
        svg_view.src = "data:image/svg+xml;utf8," + svg_data.replace("\n", "")
        svg_view.expand = True
        svg_view.fit = ft.ImageFit.CONTAIN

        # Получаем реальные размеры SVG
        base_width, base_height = get_svg_size(svg_data)
        current_scale = 1.0
        min_scale = 0.2
        max_scale = 20.0
        scale_step = 0.2

        def zoom_in(e):
            nonlocal current_scale
            if current_scale < max_scale:
                current_scale = min(current_scale + scale_step, max_scale)
                svg_view.width = int(base_width * current_scale)
                svg_view.height = int(base_height * current_scale)
                page.update()

        def zoom_out(e):
            nonlocal current_scale
            if current_scale > min_scale:
                current_scale = max(current_scale - scale_step, min_scale)
                svg_view.width = int(base_width * current_scale)
                svg_view.height = int(base_height * current_scale)
                page.update()

        toolbar = ft.Row([
            ft.IconButton(ft.Icons.ARROW_BACK, tooltip="Назад", on_click=lambda e: go_to_screen(db_choice_screen())),
            ft.IconButton(ft.Icons.REMOVE, tooltip="Уменьшить", on_click=zoom_out),
            ft.IconButton(ft.Icons.ADD, tooltip="Увеличить", on_click=zoom_in),
        ], alignment=ft.MainAxisAlignment.CENTER)

        return ft.View(
            "/erd",
            [
                ft.Container(
                    toolbar,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    ft.Column(
                        [
                            ft.Container(
                                svg_view,
                                alignment=ft.alignment.center,
                                expand=True
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO
                    ),
                    expand=True
                ),
            ],
            can_pop=True
        )

    # Запуск с первого экрана
    go_to_screen(db_choice_screen())


if __name__ == "__main__":
    ft.app(target=main)
