# ⚙️ Functional Requirements Specification

## 1. Input Processing & Parameter Ingestion
- **FR-1.1: Web Form Ingestion (`POST /generate`)**:
  - The system shall accept standard `application/x-www-form-urlencoded` submissions containing:
    - `prompt`: String (minimum 5 characters), the overarching scenario or plot concept.
    - `character_name`: String, name of the primary protagonist.
    - `setting`: String, geographic or fictional environment.
    - `tone`: String, emotional flavor (e.g., Dramatic, Funny, Noir, Epic, Mystery).
    - `style`: String, visual artistic style (e.g., Classic Comic Book, Cyberpunk, Watercolor, Anime).
    - `gemini_api_key`: Optional string, dynamic user-supplied API key.
- **FR-1.2: Headless REST API Ingestion (`POST /generate-comic/json`)**:
  - The system shall accept JSON payloads validated via Pydantic model `PromptRequest`.
  - The system shall return a structured JSON response containing generation status, panel layout list, and absolute web path to the compiled PDF.
- **FR-1.3: Preset Scenario Injection**:
  - The web interface shall provide 1-click preset buttons (e.g., Cyberpunk Detective, Mythic Quest, Deep Space Explorer, Superhero Vigilante) that instantly populate form inputs.

---

## 2. Story Generation & AI Orchestration
- **FR-2.1: 5-Panel Storyboard Outlining**:
  - The system shall prompt Google Gemini Flash to generate a valid JSON array of exactly 5 panel dictionaries containing: `panel` (integer), `title` (string), `scene_description` (string), and `image_prompt` (string).
- **FR-2.2: Algorithmic Outline Fallback**:
  - If the Gemini API key is missing, invalid, or rate-limited, the system shall seamlessly fall back to an internal algorithmic storyboard generator extracting parameters via regex.
- **FR-2.3: Comic Narration & Character Dialogue**:
  - The system shall feed the 5-panel outline into Google Gemini Pro to draft dialogue, sound effects (*POW!*, *CRACK!*), and narrative captions.
- **FR-2.4: Algorithmic Narrative Fallback**:
  - In the event of API unavailability, the system shall produce coherent comic dialogue and captions using an algorithmic story builder.

---

## 3. Visual Illustration Pipeline
- **FR-3.1: Hierarchical Image Generation**:
  - For each panel, the system shall invoke the image generation pipeline in the following priority order:
    1. Google Imagen 3 (`imagen-3.0-generate-002` / `imagen-3.0-fast-generate-001`).
    2. Google Gemini Comic SVG Engine (rasterized to PNG).
    3. Procedural Scenic Comic Art Engine in Pillow.
- **FR-3.2: Procedural Comic Art Engine Rendering**:
  - The Pillow engine shall render authentic 768x512 PNG illustrations featuring:
    - Dynamic sky gradient tailored to environment keywords (forest, cyber, cosmos).
    - Halftone Ben-Day dot matrix pattern.
    - Cel-shaded landscape contours (mountains, trees, or futuristic skylines).
    - Silhouetted character art (adventurer with cape or creature).
    - Comic title banner and top issue category tag.
    - Outer double ink borders.
- **FR-3.3: Image Persistence**:
  - Generated panel illustrations shall be saved in `static/panels/` with unique sanitized filenames incorporating prompt hashes and timestamps.

---

## 4. Layout & PDF Compilation
- **FR-4.1: Sequential Layout Binding**:
  - The system shall map image paths, titles, dialogue scripts, captions, and descriptions into a unified list of panel objects.
- **FR-4.2: Publication-Ready Multi-Page PDF Exporter**:
  - The system shall render a multi-page A4 PDF using `fpdf2`.
  - Each page shall represent one comic panel featuring:
    - Double ink outer frame.
    - Comic yellow top title bar.
    - Centered bordered comic panel illustration.
    - Scene description box with vintage paper tint.
    - Formatted dialogue and narration text using custom TrueType comic fonts (`comic.ttf`, `comicbd.ttf`).
  - The PDF shall be saved to `static/exports/comic_{timestamp}.pdf`.

---

## 5. User Interface & Archival
- **FR-5.1: Interactive Sequential Preview Reader**:
  - The system shall display the generated 5 panels in an authentic comic card reader (`comic_preview.html`) with action starbursts, responsive images, speech bubbles, and instant PDF download triggers.
- **FR-5.2: Comic Vault / Archive Gallery (`/all-users`, `/gallery`)**:
  - The system shall scan `static/exports/` and display a reverse-chronological gallery of all created comic issues with timestamps, file sizes, and download links.
- **FR-5.3: In-Browser Gemini API Key Persistence (`POST /api/save-key`)**:
  - Users shall be able to save their Gemini API key directly from the browser; the key is validated and written to `.env` and environment variables.
- **FR-5.4: Secure PDF File Download (`GET /download-pdf`)**:
  - The system shall serve requested PDFs while verifying file location to prevent directory traversal attacks.
