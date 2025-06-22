import json
import os
import re
import uuid

from src.main.persistence import Dialect, Connection
from src.main.persistence.inspector import DatabaseSchemaInspector
from src.main.visualizer import GraphvizDatabaseSchemaVisualizer


def save_connection_history(history):
    serializable_history = []

    for h in history:
        h_copy = h.copy()
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
    inspector = DatabaseSchemaInspector(conn)
    visualizer = GraphvizDatabaseSchemaVisualizer(inspector.get_tables())
    visualizer.visualize()
    with open("./erd.svg", "r") as f:
        return f.read()


def get_svg_size(svg_text):
    match = re.search(r'<svg[^>]*width="([\d.]+)[a-zA-Z]*"[^>]*height="([\d.]+)[a-zA-Z]*"', svg_text)

    width = float(match.group(1))
    height = float(match.group(2))

    return width, height