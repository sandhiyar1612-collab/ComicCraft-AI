# 💻 Phase 5: Project Development

## Overview
This phase houses the complete source code, subsystem packages, architecture layers, configuration managers, and engineering notes for **ComicCraft**.

---

## Directory Organization

```
05_Project_Development_Phase/
├── README.md                 # Development phase index & execution instructions
├── development_notes.md      # Engineering notes, technical decisions, and lessons learned
├── config/                   # Configuration management & environment variable loader
│   ├── __init__.py
│   └── settings.py
├── database/                 # Filesystem storage manager & future SQL schema blueprints
│   ├── __init__.py
│   ├── storage_manager.py
│   ├── schema.sql
│   └── README.md
├── api/                      # REST & Web controllers, routes, and Pydantic schemas
│   ├── __init__.py
│   ├── routes.py
│   └── schemas.py
├── backend/                  # Core generative engines & document compilers
│   ├── __init__.py
│   ├── gemini_flash.py       # 5-panel storyboard outline planner
│   ├── gemini_pro.py         # Narration, dialogue, and SFX script engine
│   ├── image_generator.py    # Triple-tier comic illustration engine
│   ├── layout_builder.py     # Layout aggregator and data binder
│   └── exporters.py          # FPDF2 publication PDF compiler
├── frontend/                 # Presentation layer assets & templates
│   ├── templates/            # Jinja2 HTML templates
│   └── static/               # CSS, comic TTF fonts, panels, and exports
└── source/                   # Complete runnable unified source package
    ├── __init__.py
    ├── main.py
    └── run.py
```

---

## Subsystem Highlights

1. **Configuration (`config/`)**: Centralized Pydantic/dotenv settings manager isolating environment variables, host/port settings, and directory paths.
2. **Database & Storage (`database/`)**: Clean filesystem abstraction (`StorageManager`) managing PDF exports and panel image persistence, paired with a future relational SQL schema blueprint.
3. **API & Controllers (`api/`)**: Web endpoints, form processors, RESTful JSON generator (`/generate-comic/json`), and API key manager.
4. **Backend Subsystems (`backend/`)**: AI model integrations, intelligent fallbacks, procedural Pillow Ben-Day dot engine, and publication-ready PDF generator.
5. **Frontend Subsystems (`frontend/`)**: Authentic vintage comic paper design system, Google Fonts typography, and responsive templates.

---

## Running the Application
From the repository root:
```bash
# Using the root launcher
python run.py

# Or via Uvicorn directly
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.
Interactive API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
