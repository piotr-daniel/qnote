## QNote Roadmap

A forward-looking plan for upcoming releases and long-term development.

This roadmap is intentionally high-level. Individual tasks will be tracked as GitHub Issues and grouped using Milestones.

### 🔹 0.1.x - UI & Widget Polish (Next Minor Release)
Core goals

- Add search/filter widget
- Add Settings to control themes, Lumen, possibly more
- New note highlight colour
- Add keyboard cheatsheet (?)
- Possible Extras

### 🔹 0.2.x - Themes & Appearance
Core Goals

- Theme switching UI
- Include built-in themes:
  - Solarized
  - Cyberpunk
  - Monochrome (minimalist)
  - High-contrast accessibility theme
- More *Lumens*:
  - QNote Logo
  - Snake
  - Breakout


### 🔹 0.3.x - Storage & Data Model Improvements
Core Goals

- Export data:
  - JSON
  - YAML
  - Other directory
- Backup
- Autosave


### 🔹 0.4.x - Note Management & Features
Core Goals

- Tagging system
- Filtering + searching UI
- Pinned notes
- Link to other note
- ToDo/Tasks


### 🔹 0.5.x - Quality of Life
Core Goals

- Crash recovery (auto-save to temp file)
- Log file management:
  - ~/.local/state/qnote/qnote.log


### 🔹 0.6.x — Extensibility
Core Goals

- Custom storage backends
- Commands / keybindings


### 🔹 1.0.0 — Stable API & UX

The 1.0 release focuses on stability.

Core Goals

- Stabilise internal APIs
- Widgets
- Storage
- Hooks/extensions
- Polish all rough UI edges
- Comprehensive documentation:
  - Widget docs
  - Theme creation
  - Architecture overview
- Full test suite coverage for:
  - CRUD
  - Widgets
  - Config
  - Storage services
- Accessibility review (colors, keybindings, screen reader compatibility where possible)

Long-Term Ideas (Not Tied to Version)

These are ideas, not commitments:
- Multi-window/tabs support
- Cloud sync using a provider plugin (e.g., Dropbox, GitHub Gist, WebDAV, S3)
- Embedded calendar widget
- Kanban layout mode
- AI-augmented features (summaries, tag suggestions)