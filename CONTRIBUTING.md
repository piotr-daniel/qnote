## Contributing to QNote

Thank you for your interest in improving *QNote* — a fast, expressive TUI note-taking app built with Textual.
Contributions of all kinds are welcome: bug fixes, new widgets, documentation, themes, or feature ideas.

Please read this guide before opening issues or pull requests.

### Ways to Contribute

- Report bugs
- Suggest enhancements or features
- Improve documentation
- Add tests
- Contribute widgets, UI polish, themes
- Help improve performance or stability

### Development
```bash
git clone https://github.com/piotr-daniel/qnote.git
cd qnote
python -m venv .venv
# .venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -e .
qnote  # launch the app
```

---

### Submitting Issues

Please include:

- A clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Platform info (OS, Python version)
- Screenshots or GIFs when helpful

---

### Adding Widgets or UI Components

All custom widgets live in:

```
qnote/widgets/
```

When adding or modifying a widget:
- Keep logic minimal — offload heavy work to services.
- Add a short docstring explaining the widget’s purpose.
- Add a simple test under tests/test_widgets.py.
- If applicable, update the README screenshot or widget examples.

---

### Roadmap

High-level future plans are kept in [ROADMAP](ROADMAP.md)

Feel free to propose additions or ideas via issues or PRs but please check ROADMAP *before* doing so
to avoid duplication. 