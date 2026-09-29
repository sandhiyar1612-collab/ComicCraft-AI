# 📖 Use Cases Specification

## Use Case Summary Table

| Use Case ID | Name | Primary Actor | Trigger |
| :--- | :--- | :--- | :--- |
| **UC-01** | Create Comic via Web Interface | End User / Storyteller | Submits form on `/` |
| **UC-02** | Generate Comic via REST API | External Client / Automated Script | `POST /generate-comic/json` |
| **UC-03** | Use 1-Click Creative Presets | End User | Clicks a preset pill on `/` |
| **UC-04** | Browse & Download from Comic Vault | End User / Reader | Visits `/all-users` or `/gallery` |
| **UC-05** | Save Gemini API Key Dynamically | End User / Developer | Clicks "Save Key" in UI |
| **UC-06** | Run Image Engine Smoke Test | Developer / QA | Calls `GET /test-image` |

---

## Detailed Use Cases

### UC-01: Create Comic via Web Interface
- **Primary Actor**: Storyteller / End User.
- **Preconditions**: ComicCraft web server is running; user navigates to `http://127.0.0.1:8000`.
- **Main Success Scenario**:
  1. User fills in: Story Prompt, Character Name, Setting, Tone, and Art Style.
  2. User optionally provides or verifies their Google Gemini API Key.
  3. User clicks the "CREATE COMIC BOOK" button.
  4. The UI triggers the comic flipbook loading modal.
  5. The server orchestrates:
     - `generate_outline`: Creates 5-panel storyboard breakdown.
     - `generate_story`: Crafts dialogue, captions, and sound effects.
     - `generate_image`: Renders 5 panel illustrations.
     - `build_comic_layout`: Binds text and image components.
     - `save_pdf`: Compiles multi-page PDF in `static/exports/`.
  6. The server renders `comic_preview.html`.
  7. User views the 5 sequential panels, reads the narrative, and clicks "DOWNLOAD PRINTABLE PDF".
- **Alternative Flow (Offline / Rate-Limited Fallback)**:
  - At Step 5, if the Gemini API key is missing or quota is exhausted, the system automatically engages the internal algorithmic outline and story generators and Pillow scenic comic engine. Generation completes within 3 seconds, and a complete valid comic is rendered without error.

---

### UC-02: Generate Comic via REST API
- **Primary Actor**: Automated Client, CLI, or Mobile Application.
- **Preconditions**: Client has network access to the API endpoint.
- **Main Success Scenario**:
  1. Client sends HTTP POST to `/generate-comic/json` with JSON body:
     ```json
     {
       "prompt": "A courageous astronaut stranded on an alien moon",
       "character_name": "Commander Vance",
       "setting": "Lunar Obsidian Crater",
       "tone": "Suspenseful and Heroic",
       "style": "Retro Sci-Fi Comic"
     }
     ```
  2. Server validates payload via Pydantic model `PromptRequest`.
  3. Server executes generation pipeline.
  4. Server responds with HTTP 200 and JSON payload:
     ```json
     {
       "status": "success",
       "layout": [...],
       "pdf_path": "/static/exports/comic_20260928115817.pdf"
     }
     ```

---

### UC-03: Browse & Download from Comic Vault
- **Primary Actor**: Comic Reader / Archivist.
- **Preconditions**: At least one comic has been generated.
- **Main Success Scenario**:
  1. User clicks the "Comic Vault" link in the top navigation bar or visits `/all-users`.
  2. The server scans `static/exports/*.pdf` and retrieves file modification timestamps and sizes.
  3. The server renders `all_users.html` with an issue grid.
  4. User clicks "Download Issue" on any listed comic.
  5. Route `/download-pdf?file_path=...` validates that the path is within `static/exports/` and streams the PDF file to the browser with proper headers (`Content-Disposition: attachment`).
