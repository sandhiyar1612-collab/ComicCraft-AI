# 📋 Development Plan

## 1. Development Methodology
ComicCraft was developed following an **Agile / Iterative Sprint Framework**. Each sprint focused on delivering an independently testable component of the comic generation pipeline, prioritizing early risk mitigation and deterministic fallbacks.

---

## 2. Sprint Roadmap

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SPRINT ROADMAP OVERVIEW                         │
├──────────┬─────────────────────────────────────────────────────────────┤
│ Sprint 1 │ Architecture Setup & Outline Generation (Gemini Flash)      │
│ Sprint 2 │ Narrative Scripting & Dialogue Writing (Gemini Pro)         │
│ Sprint 3 │ Multi-Tier Visual Generation & Ben-Day Halftone Engine      │
│ Sprint 4 │ Layout Builder & FPDF2 Publication PDF Exporter             │
│ Sprint 5 │ Authentic Vintage Comic Paper Frontend & Comic Vault        │
│ Sprint 6 │ Hardening, Automated Test Suite, Phase Docs & Deployment    │
└──────────┴─────────────────────────────────────────────────────────────┘
```

### Sprint 1: Core Foundation & Story Outlining
- **Goals**: Set up project workspace, FastAPI app skeleton, and Gemini Flash outline generator.
- **Deliverables**:
  - `app/main.py` and `app/routes.py` basic skeleton.
  - `app/gemini_flash.py` with strict JSON schema parsing and regex-based offline fallback.
  - Unit tests verifying JSON outline extraction.

### Sprint 2: Scripting, Dialogue & Sound Effects
- **Goals**: Implement rich dialogue crafting and multi-character storytelling.
- **Deliverables**:
  - `app/gemini_pro.py` orchestrating Gemini 1.5 Pro.
  - Atmospheric caption, character dialogue, and sound effect (*POW!*, *CRACK!*) prompts.
  - Script formatting and fallback narrative generators.

### Sprint 3: Visual Generation Pipeline
- **Goals**: Build reliable comic panel visualization with zero-fail guarantee.
- **Deliverables**:
  - `app/image_generator.py` with 3-tier fallback (Imagen 3 ──► Gemini SVG ──► Pillow Scenic Engine).
  - Procedural 768x512 comic scene drawing with layered sky gradients, Ben-Day dot matrices, celestial bodies, and silhouette hero character art.
  - Panel asset persistence in `static/panels/`.

### Sprint 4: Layout Binding & PDF Exporter
- **Goals**: Bind textual and visual assets into publication-ready documents.
- **Deliverables**:
  - `app/layout_builder.py` aggregating outline, story script, and panel images.
  - `app/exporters.py` using `fpdf2` and TrueType comic fonts (`comic.ttf`, `comicbd.ttf`).
  - Automated page framing, yellow header banners, and Latin-1 character sanitization.

### Sprint 5: Authentic Comic Paper UI & Archival Vault
- **Goals**: Design and implement the vintage comic aesthetic and gallery.
- **Deliverables**:
  - `static/css/comic.css` with halftone dot background and ink borders.
  - `templates/index.html` with 1-click presets and dynamic API key configurator.
  - `templates/comic_preview.html` sequential comic reader.
  - `templates/all_users.html` Comic Vault archive gallery.

### Sprint 6: Hardening, Automated Testing & Documentation
- **Goals**: Formalize phase-wise repository organization, automated test suite, and deployment packages.
- **Deliverables**:
  - Complete Phase 01 through Phase 08 repository structure.
  - Automated test suite in `06_Project_Testing_Phase/` with 100% component coverage.
  - Containerization configurations (`Dockerfile`, `docker-compose.yml`).
  - Comprehensive user and developer documentation.

---

## 3. Risk Management Matrix

| Risk Event | Severity | Probability | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Gemini API Quota Exceeded / 429 Errors** | High | High | Implement deterministic local algorithmic story and outline generators. |
| **Imagen 3 Deprecation or Restriction** | High | High | Multi-tier failover to Gemini SVG and native procedural Pillow Ben-Day Scenic comic engine. |
| **Special Unicode Characters Breaking PDF** | Medium | Medium | Implement `clean_text_for_pdf()` to replace smart quotes, dashes, and accents with Latin-1 equivalents. |
| **Directory Traversal in PDF Download** | High | Low | Enforce strict path prefix validation (`os.path.normpath().startswith('static/exports')`). |
