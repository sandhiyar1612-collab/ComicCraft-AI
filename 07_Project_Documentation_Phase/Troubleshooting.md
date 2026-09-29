# 🔧 Troubleshooting & Diagnostics Guide

This document lists common operational issues, diagnostic commands, and verified remedies.

---

## 1. Port 8000 Already in Use
- **Symptom**: `OSError: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)`.
- **Cause**: Another service or a previously running Uvicorn process is occupying port 8000.
- **Resolution**:
  - **Windows (PowerShell)**:
    ```powershell
    Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
    ```
  - **Linux / macOS**:
    ```bash
    lsof -ti:8000 | xargs kill -9
    ```
  - Alternatively, launch on another port:
    ```bash
    uvicorn app.main:app --port 8080 --reload
    ```

---

## 2. Gemini API Key Quota Exceeded or Rate Throttling (HTTP 429)
- **Symptom**: Console outputs: `[WARNING] Gemini Flash generation notice: 429 Resource has been exhausted`.
- **Behavior**: ComicCraft automatically catches the quota exception and invokes its internal algorithmic story and outline generators. The user still receives a complete 5-panel comic without interruption.
- **Resolution**:
  - Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to check project quota.
  - Switch or update keys in `.env` or directly through the web UI key configurator.

---

## 3. Imagen 3 Model 404 in Developer API Mode
- **Symptom**: Console notice: `[GEMINI REST] imagen-3.0-generate-002 response status: 404`.
- **Cause**: Google restricts direct Imagen 3 diffusion inference to Enterprise Agent Platform mode for certain developer keys.
- **Behavior**: ComicCraft detects the status and automatically switches to the built-in Pillow Procedural Scenic Comic Art Engine, rendering high-res Ben-Day halftone panels.
- **Resolution**: No manual action needed — ComicCraft is designed to run with 100% uptime using local procedural drawing.

---

## 4. Missing Custom Comic Fonts (`comic.ttf`)
- **Symptom**: Console log: `Font loading error, using Helvetica: [Errno 2] No such file or directory: 'static/fonts/comic.ttf'`.
- **Behavior**: The PDF exporter automatically falls back to standard `Helvetica` without breaking PDF compilation.
- **Resolution**: Ensure TrueType fonts (`comic.ttf`, `comicbd.ttf`) are present in `static/fonts/`.

---

## 5. Directory Traversal Security Warning (HTTP 400)
- **Symptom**: Accessing `/download-pdf?file_path=../../etc/passwd` returns `HTTP 400: Invalid file path: Security violation`.
- **Cause**: The application actively defends against path traversal.
- **Resolution**: Only request files located within `static/exports/` (e.g., `/download-pdf?file_path=static/exports/comic_20260928115817.pdf`).

---

## 6. Permission Denied Creating `static/exports/`
- **Symptom**: `PermissionError: [Errno 13] Permission denied: 'static/exports'`.
- **Resolution**: Ensure the user running the process has write permissions:
  ```bash
  sudo chown -R $USER:$USER static/
  chmod -R 755 static/
  ```
