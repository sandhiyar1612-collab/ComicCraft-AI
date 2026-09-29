# 🛡️ Non-Functional Requirements Specification

## 1. Performance & Latency
- **NFR-1.1: Local Fallback Execution Speed**: When operating in fallback mode (or when third-party APIs are unresponsive), the end-to-end generation of 5 panels, text layout, and PDF compilation shall complete within **< 3.0 seconds**.
- **NFR-1.2: Cloud AI Latency Handling**: When communicating with Google Gemini and Imagen APIs, HTTP request timeouts shall be capped at 20 seconds per model call. The UI shall display an animated comic flipbook loading state to prevent perceived stall.
- **NFR-1.3: PDF Generation Overhead**: The `fpdf2` rendering pipeline shall generate a complete 5-page publication-ready PDF in **< 400 milliseconds**.
- **NFR-1.4: Lightweight Resource Footprint**: The application shall operate effectively on low-spec host systems with as little as 512MB RAM without requiring local GPU acceleration.

---

## 2. Reliability & Fault Tolerance
- **NFR-2.1: Zero-Crash Architecture**: The application shall never crash or return unhandled 500 error pages due to external AI rate limits, missing API keys, or API schema changes.
- **NFR-2.2: Deterministic Cascading Fallbacks**:
  - Outline Generation: Gemini Flash ──► Regex Story Outline Fallback.
  - Story Generation: Gemini Pro ──► Comic Dialogue Script Fallback.
  - Image Generation: Imagen 3 ──► Gemini SVG ──► Pillow Ben-Day Scenic Engine.
  - Font Loading: Custom Comic TTF ──► Core Helvetica.
- **NFR-2.3: Automatic Directory Provisioning**: At application startup, the system shall ensure all necessary asset folders (`static/panels`, `static/exports`, `static/fonts`, `static/css`, `static/img`) exist or are automatically created.

---

## 3. Security & Safety
- **NFR-3.1: Directory Traversal Mitigation**: The file download route (`/download-pdf`) shall sanitize incoming path parameters, strictly verifying that normalized paths remain confined inside `static/exports/`. Attempted directory traversal (e.g., `../../etc/passwd` or `..\Windows\System32`) shall be rejected with HTTP 400.
- **NFR-3.2: API Key Protection**:
  - The default `.gitignore` shall strictly exclude `.env` to prevent accidental credential leakage into public GitHub repositories.
  - The UI shall mask the Gemini API key input using password field masking.
- **NFR-3.3: Filename Sanitization**: Image filenames shall be sanitized with alphanumeric filters and MD5 hashes to prevent shell injection or illegal filesystem character errors across Windows and Linux.

---

## 4. Usability & User Experience (UX)
- **NFR-4.1: Responsive Viewport Adaptation**: The user interface shall dynamically adapt across desktop monitors, tablets, and mobile smartphones (from 320px width up to 4K displays).
- **NFR-4.2: Comic Aesthetic Integrity**: The interface shall strictly maintain the vintage American comic paper aesthetic:
  - Cream/parchment background (`#faf6ea`).
  - Ben-Day halftone dot pattern matrices.
  - Heavy black ink borders (`3.5px solid #18181b`).
  - Retro offset drop shadows (`6px 6px 0px #18181b`).
  - Google typography (`Bangers`, `Comic Neue`, `Permanent Marker`, `Outfit`).
- **NFR-4.3: Low Cognitive Load**: First-time users shall be able to generate a comic with zero manual typing using pre-configured 1-click creative presets.

---

## 5. Maintainability & Code Quality
- **NFR-5.1: Modular Separation of Concerns**: Logic shall be partitioned into single-responsibility Python modules (`gemini_flash.py`, `gemini_pro.py`, `image_generator.py`, `layout_builder.py`, `exporters.py`, `routes.py`).
- **NFR-5.2: Self-Documenting REST API**: All REST endpoints shall automatically expose interactive OpenAPI specifications accessible via `/docs` (Swagger UI) and `/redoc` (ReDoc).
- **NFR-5.3: Type Safety**: Data models for API requests shall use Pydantic `BaseModel` with clear field descriptions and constraints.
