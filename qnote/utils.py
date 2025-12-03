import sqlite3
import json

from appdirs import user_data_dir
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(user_data_dir("qnote"))
DATA_FILE = DATA_DIR / "data.db"

SETTINGS = {}

def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATA_FILE)


def init_db():
    """Initialize the database."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)


def add_note(title: str, content: str, category: str, tags: list = None):
    """Add a new note to database."""

    tags_json = json.dumps(tags) if tags else None

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO notes (title, content, category, tags, updated) VALUES (?, ?, ?, ?, ?)",
            (
                title,
                content,
                category,
                tags_json,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )


def delete_note(note_id):
    """Delete note from database."""
    with get_connection() as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))


def update_note_content(note_id, new_content):
    """Update the content of a note."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE notes SET content = ?, updated = ? WHERE id = ?",
            (new_content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), note_id),
        )


def update_note_title(note_id, new_title):
    """Update the title of a note."""
    with get_connection() as conn:
        conn.execute("UPDATE notes SET title = ? WHERE id = ?", (new_title, note_id))


def update_note_category(note_id, new_category):
    """Update the category of a note."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE notes SET category = ? WHERE id = ?", (new_category, note_id)
        )


def get_note(note_id):
    """Get all notes from database."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM notes WHERE id = ?", note_id)
        return cursor.fetchone()


def get_notes(text: str=None) -> list:
    """Get all notes from database."""
    with get_connection() as conn:
        if text:
            cursor = conn.execute(
                "SELECT * FROM notes WHERE title LIKE ? OR category LIKE ? OR content LIKE ? ORDER BY updated DESC;",
                ("%"+text+"%", "%"+text+"%", "%"+text+"%")
            )
        else:
            cursor = conn.execute("SELECT * FROM notes ORDER BY updated DESC;")
        return cursor.fetchall()


def get_categories():
    """Get distinct categories from database. If there are no categories, return General as default."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT DISTINCT category FROM notes;")
        categories = [c[0] for c in cursor.fetchall()]
        if not categories:
            categories.append("New Notes")
        categories.sort()
        return categories


def load_all_settings():
    with get_connection() as conn:
        for key, value in conn.execute("SELECT key,value FROM settings"):
            try:
                SETTINGS[key] = json.loads(value)
            except IndexError:
                SETTINGS[key] = value


def get_setting(key, default=None):
    return SETTINGS.get(key, default)


def set_setting(key, value):
    SETTINGS[key] = value
    with get_connection() as conn:
        conn.execute("INSERT OR REPLACE INTO settings VALUES (?,?)", (key, json.dumps(value)))
