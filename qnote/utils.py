import json
import logging
import uuid
import datetime
from pathlib import Path


DATA_DIR = Path.home() / ".qnote"
DATA_FILE = DATA_DIR / "data.json"

def load_notes():
    """Load all notes from the JSON file. Return a list."""
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # In case of file corruption or empty file
        return []

def save_notes(notes):
    """Write notes safely to JSON file. Create file if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp_file = DATA_FILE.with_suffix(".tmp")

    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

    tmp_file.replace(DATA_FILE)  # Atomic replace

def add_note(title: str, content: str, tags=None):
    """Add a new note to data.json."""
    #  title to be auto generated with first few words or later edited by user
    #  future dev: tags to be auto generated
    notes = load_notes()
    new_note = {
        "id": str(uuid.uuid4()),
        "title": title,
        "content": content,
        "tags": tags or [],
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    notes.append(new_note)
    save_notes(notes)
    return new_note


def save_note(id: str, title: str, content: str, tags=None):
    """Save a note to data.json."""
    notes = load_notes()
    for idx, note in enumerate(notes):
        if note["id"] == id:
            notes[idx]["title"] = title
            notes[idx]["content"] = content
            break
    save_notes(notes)