import logging
import sqlite3
from pathlib import Path

DATA_DIR = Path.home() / ".qnote"
DATA_FILE = DATA_DIR / "data.db"


def get_connection():
    return sqlite3.connect(DATA_FILE)


def init_db():
    """Initialize the database."""
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)


def add_note(title: str, content: str, category: str="General", tags: list=None):
    """Add a new note to database."""
    tags_str = ",".join(tags) if tags else None
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO notes (title, content, category, tags) VALUES (?, ?, ?, ?)",
            (title, content, category, tags_str)
        )


def delete_note(note_id):
    """Delete note from database."""
    with get_connection() as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))


def update_note(note_id, new_content):
    """Update the content of a note."""
    with get_connection() as conn:
        conn.execute("UPDATE notes SET content = ? WHERE id = ?", (new_content, note_id))


def get_notes():
    """Get all notes from database."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM notes ORDER BY created DESC")
        return cursor.fetchall()


def get_categories():
    """Get distinct categories from database."""
    with get_connection() as conn:
        cursor = conn.execute("SELECT DISTINCT category FROM notes ORDER BY created DESC")
        return cursor.fetchall()
