# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly is a Flask-based personal expense tracker web application. It uses SQLite for data storage, Jinja2 templates, and vanilla JS for interactivity. The app runs on port 5001 in debug mode.

## Commands

```bash
# Run the app
./venv/Scripts/python app.py

# Run tests
./venv/Scripts/python -m pytest

# Run a single test file
./venv/Scripts/python -m pytest tests/test_filename.py
```

## Architecture

- **Single-file Flask app** — `app.py` contains all routes. Routes with `"— coming in Step X"` comments are placeholders for a multi-step implementation.
- **Database layer** — `database/db.py` is scaffolded but empty (students implement `get_db()`, `init_db()`, and `seed_db()`). Import it via `from database import db`.
- **Templates** — Jinja2 templates in `templates/`. All pages extend `base.html` which provides the navbar, footer, and static asset links.
- **Static assets** — CSS in `static/css/style.css`, JS in `static/js/main.js`.
- **Database file** — `expense_tracker.db` (gitignored) is the SQLite database.

## Design

- Font stack: DM Serif Display (headings) + DM Sans (body) via Google Fonts
- Brand: ◈ Spendly
- Color system: CSS variables (see `static/css/style.css`)

## Key Routes in app.py

| Route | Handler | Status |
|---|---|---|
| `/` | `landing()` | Implemented |
| `/register` | `register()` | Implemented |
| `/login` | `login()` | Implemented |
| `/terms`, `/privacy` | Static pages | Implemented |
| `/logout`, `/profile`, `/expenses/*` | Placeholders | Not implemented |

## Environment

- Python virtual environment is in `venv/`
- Dependencies: Flask 3.1.3, Werkzeug 3.1.6, pytest 8.3.5, pytest-flask 1.3.0
- Database cursor uses `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
