# QNote

QNote is a terminal-based, local-first, note-taking app powered by [Textual](https://github.com/Textualize/textual).  
It provides a fast, intuitive, and visually appealing way to manage your notes directly in the terminal.

[![Demo](demo.gif)](demo.mp4)
---

## Features

- **Terminal UI**: Sidebar, stats panel with *Lumen* - a visual widget, and content area for easy navigation and editing.
- **SQLite backend**: Persistent note storage with fast queries.
- **Cross-platform**: Works on Windows, macOS, and Linux.
- **Console script**: Launch with `qnote` after installation.

---

## Installation

### Using pip (recommended)

```bash
pip install qnote
```

---

## Development
```bash
git clone https://github.com/piotr-daniel/qnote.git
cd qnote
python -m venv .venv
# .venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -e .
qnote  # launch the app
```
