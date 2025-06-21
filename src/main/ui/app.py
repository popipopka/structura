import uuid

import flet as ft

from src.main.persistence import DatabaseURL, Dialect, Connection
from src.main.ui import load_connection_history, DatabaseCard, save_connection_history, ConnectionHistoryCard, \
    generate_erd_svg, get_svg_size


def app(page: ft.Page):
    page.title = "Structura"
    page.window_width = 900
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK

    # Состояние
    connection_history = load_connection_history()
    current_db_url = None
    svg_data = None
    error_text = ft.Text("", color=ft.Colors.RED, text_align=ft.TextAlign.CENTER, max_lines=8)

    def go_to_screen(screen):
        page.views.clear()
        page.views.append(screen)
        error_text.value = ""
        page.update()

    # --- Экран 1: Стартовый экран ---
    def db_choice_screen():
        db_cards = [
            DatabaseCard(
                name=Dialect.POSTGRESQL.value.upper(),
                dialect=Dialect.POSTGRESQL,
                on_select=lambda dialect: go_to_screen(connection_input_screen(dialect))
            ),
            DatabaseCard(
                name=Dialect.MARIADB.value.upper(),
                dialect=Dialect.MARIADB,
                on_select=lambda dialect: go_to_screen(connection_input_screen(dialect))
            ),
            DatabaseCard(
                name=Dialect.MYSQL.value.upper(),
                dialect=Dialect.MYSQL,
                on_select=lambda dialect: go_to_screen(connection_input_screen(dialect))
            )
        ]
        db_cards_row = ft.Row(db_cards, alignment=ft.MainAxisAlignment.CENTER, spacing=24)

        def delete_history(connection_uuid):
            connection_history[:] = [h for h in connection_history if h.get('uuid') != connection_uuid]
            save_connection_history(connection_history)
            go_to_screen(db_choice_screen())

        def quick_connect(h):
            nonlocal current_db_url
            try:
                dialect: Dialect = h.get('dialect')
                current_db_url = DatabaseURL(
                    dialect, h['user'], h['password'], h['host'], h['port'], h['database']
                )
                conn = Connection(current_db_url)
                conn.get_engine().connect().close()
                error_text.value = ""
                go_to_screen(erd_screen())
            except Exception as ex:
                error_text.value = f"Ошибка подключения: {ex}"
                page.update()

        history_cards = [
            ConnectionHistoryCard(
                history=h,
                on_delete=delete_history,
                on_select=quick_connect,
                on_edit=lambda h: go_to_screen(connection_edit_screen(h))
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
                    expand_loose=True
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
                ),
                ft.Container(
                    error_text,
                    alignment=ft.alignment.center,
                )
            ]
        )

    # --- Экран 2: Ввод данных соединения ---
    def connection_input_screen(dialect):
        card_width = 400
        field_height = 44
        host = ft.TextField(label="Хост", value="localhost", height=field_height, width=card_width * 0.65)
        port = ft.TextField(label="Порт", value="5432", height=field_height, expand=True)
        user = ft.TextField(label="Пользователь", value=dialect.value, height=field_height, width=card_width)
        password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, height=field_height,
                                width=card_width)
        database = ft.TextField(label="База данных", height=field_height, width=card_width)

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
                        ft.Column(
                            [
                                ft.Text("Введите данные для подключения", size=20, weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Row(
                                    [
                                        host,
                                        port
                                    ],
                                    spacing=8,
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                user,
                                password,
                                database,
                                error_text,
                                ft.Row(
                                    [
                                        ft.OutlinedButton("Назад", on_click=lambda e: go_to_screen(db_choice_screen()),
                                                          expand=True, height=field_height),
                                        ft.FilledButton("Принять", on_click=on_accept, expand=True,
                                                        height=field_height),
                                    ],
                                    spacing=8
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12
                        ),
                        padding=28,
                        width=card_width,
                        alignment=ft.alignment.center,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )

    # --- Экран 3: ERD SVG ---
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

        def reset_view(e):
            nonlocal current_scale
            current_scale = 1.0
            svg_view.width = int(base_width * current_scale)
            svg_view.height = int(base_height * current_scale)
            page.update()

        toolbar = ft.Row(
            [
                ft.TextButton(
                    "Назад",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: go_to_screen(db_choice_screen()),
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(horizontal=16, vertical=8)
                    )
                ),
                ft.Row(
                    [
                        ft.IconButton(ft.Icons.REMOVE, tooltip="Уменьшить", on_click=zoom_out),
                        ft.IconButton(ft.Icons.ADD, tooltip="Увеличить", on_click=zoom_in),
                        ft.IconButton(ft.Icons.REFRESH, tooltip="Сбросить", on_click=reset_view),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8
                ),
                ft.Container(width=80)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

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
                            ft.Row(
                                [
                                    ft.Container(
                                        svg_view,
                                        alignment=ft.alignment.center,
                                        expand=True
                                    )
                                ],
                                scroll=ft.ScrollMode.AUTO,
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                ),
            ]
        )

    # --- Экран 4: Редактирование соединения ---
    def connection_edit_screen(history):
        card_width = 400
        field_height = 44
        host = ft.TextField(label="Хост", value=history['host'], height=field_height, width=card_width * 0.65)
        port = ft.TextField(label="Порт", value=str(history['port']), height=field_height, expand=True)
        user = ft.TextField(label="Пользователь", value=history['user'], height=field_height, width=card_width)
        password = ft.TextField(label="Пароль", value=history['password'], password=True, can_reveal_password=True,
                                height=field_height, width=card_width)
        database = ft.TextField(label="База данных", value=history['database'], height=field_height, width=card_width)

        def on_accept(e):
            if not all([host.value, port.value, user.value, password.value, database.value]):
                error_text.value = "Все поля должны быть заполнены!"
                page.update()
                return
            try:
                db_url = DatabaseURL(history['dialect'], user.value, password.value, host.value, int(port.value),
                                     database.value)
                conn = Connection(db_url)
                conn.get_engine().connect().close()

                for h in connection_history:
                    if h.get('uuid') == history.get('uuid'):
                        h.update({
                            'user': user.value,
                            'password': password.value,
                            'host': host.value,
                            'port': int(port.value),
                            'database': database.value,
                            'dialect': history['dialect']
                        })
                        break
                save_connection_history(connection_history)
                go_to_screen(db_choice_screen())
            except Exception as ex:
                error_text.value = f"Ошибка подключения: {ex}"
                page.update()

        return ft.View(
            "/connection_edit",
            [
                ft.Container(
                    content=ft.Container(
                        ft.Column([
                            ft.Text("Изменить данные для подключения", size=20, weight=ft.FontWeight.BOLD,
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
                                ft.OutlinedButton("Отмена", on_click=lambda e: go_to_screen(db_choice_screen()),
                                                  expand=True, height=field_height),
                                ft.FilledButton("Принять", on_click=on_accept, expand=True, height=field_height),
                            ], spacing=8),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
                            spacing=12),
                        padding=28,
                        width=card_width,
                        alignment=ft.alignment.center,
                    ),
                    alignment=ft.alignment.center,
                    expand=True
                )
            ]
        )

    # Запуск с первого экрана
    go_to_screen(db_choice_screen())
