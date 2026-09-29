# 🧪 Detailed Test Cases

## Test Case Matrix

| Test Case ID | Test Category | Target Component | Priority | Automated |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Unit | `app.gemini_flash._generate_fallback_outline` | High | Yes |
| **TC-02** | Unit | `app.gemini_pro._generate_fallback_story` | High | Yes |
| **TC-03** | Unit | `app.image_generator.sanitize_filename` | High | Yes |
| **TC-04** | Integration | `app.image_generator._draw_comic_scenic_image` | High | Yes |
| **TC-05** | Integration | `app.layout_builder.build_comic_layout` | High | Yes |
| **TC-06** | Unit | `app.exporters.clean_text_for_pdf` | High | Yes |
| **TC-07** | Integration | `app.exporters.save_pdf` | High | Yes |
| **TC-08** | Security | `05_Project_Development_Phase.database.storage_manager` | Critical | Yes |
| **TC-09** | API Contract | `app.routes` & `app.main` (FastAPI TestClient) | High | Yes |

---

## Detailed Specifications

### TC-01: Outline Fallback Structure & Key Validation
- **Objective**: Verify that the algorithmic outline generator produces exactly 5 valid panels with all mandatory dictionary keys.
- **Input**: `"The hero is Alex in a mysterious cavern, dramatic tone, comic book style"`.
- **Preconditions**: Python environment initialized; `app.gemini_flash` loaded.
- **Execution Steps**:
  1. Invoke `_generate_fallback_outline(prompt)`.
  2. Measure output length (`len(outline)`).
  3. Validate each dictionary contains keys: `panel`, `title`, `scene_description`, `image_prompt`.
- **Expected Result**: Output is a list of exactly 5 dictionaries; panel numbers are 1 through 5; all keys are present and populated.

---

### TC-02: Narrative Story Fallback Script Validation
- **Objective**: Verify that the story script fallback produces dialogue, atmospheric captions, and narration for all panels.
- **Input**: 5-panel outline dictionary list.
- **Execution Steps**:
  1. Invoke `_generate_fallback_story(outline)`.
  2. Inspect string output for panel markers, captions, and dialogue lines.
- **Expected Result**: Output string contains `"Panel 1"` through `"Panel 5"`, `"CAPTION:"`, and `"NARRATION:"`.

---

### TC-03: Filename Sanitization & MD5 Hashing
- **Objective**: Verify that special characters, slashes, and spaces are removed to prevent filesystem and shell injection attacks.
- **Input**: `"A wild @#$%^&* test prompt with spaces and /slashes!"`.
- **Execution Steps**:
  1. Invoke `sanitize_filename(prompt)`.
  2. Inspect returned filename.
- **Expected Result**: Filename starts with `"panel_"`, ends with `".png"`, and contains no special characters like `@`, `/`, or `\`.

---

### TC-04: Procedural Halftone Comic Image Rendering
- **Objective**: Verify that the Pillow procedural engine generates an authentic, uncorrupted PNG image with exact 768x512 dimensions.
- **Input**: Prompt `"A futuristic cyber city with neon lights and a masked detective"`, destination `static/panels/test_unit_scene.png`.
- **Execution Steps**:
  1. Invoke `_draw_comic_scenic_image(prompt, destination)`.
  2. Verify file exists on disk.
  3. Open image with `PIL.Image` and inspect `.size` and `.format`.
- **Expected Result**: File is created; size is exactly `(768, 512)`; format is `"PNG"`.

---

### TC-05: Layout Builder Multi-Component Aggregation
- **Objective**: Verify that `build_comic_layout` binds image paths, titles, story scripts, and panel descriptions cleanly.
- **Input**: List of 5 image paths, story text string, 5-panel outline list.
- **Execution Steps**:
  1. Invoke `build_comic_layout(images, story, outline)`.
  2. Verify length of output list.
  3. Verify presence of keys: `panel`, `title`, `image_path`, `text`, `scene_description`.
- **Expected Result**: Returns a list of 5 structured panel dictionaries with complete properties.

---

### TC-06: PDF Unicode Character Normalization & Sanitization
- **Objective**: Verify that smart quotes, em-dashes, and special characters are converted to Latin-1 safe characters for FPDF.
- **Input**: `“Hello world” — said the hero… it’s working with café!`.
- **Execution Steps**:
  1. Invoke `clean_text_for_pdf(input_text)`.
  2. Check for absence of curly characters and presence of standard quotes and hyphens.
- **Expected Result**: Curly quotes replaced with `"` and em-dash replaced with `-`.

---

### TC-07: FPDF2 Multi-Page PDF Compilation
- **Objective**: Verify that `save_pdf` compiles a complete multi-page PDF with borders and comic fonts.
- **Input**: 5-panel compiled layout list.
- **Execution Steps**:
  1. Invoke `save_pdf(layout)`.
  2. Check returned path exists and file size > 1,000 bytes.
- **Expected Result**: PDF is successfully written to `static/exports/comic_*.pdf`; file is non-empty and valid.

---

### TC-08: Path Traversal Attack Mitigation
- **Objective**: Verify that `StorageManager.is_safe_export_path()` rejects malicious paths attempting to access system files.
- **Inputs**:
  - Safe: `static/exports/comic_123.pdf`
  - Attack 1: `static/exports/../../etc/passwd`
  - Attack 2: `..\..\Windows\System32\calc.exe`
  - Attack 3: `/etc/shadow`
- **Execution Steps**:
  1. Pass each path to `storage.is_safe_export_path()`.
  2. Assert boolean return.
- **Expected Result**: Safe path returns `True`; all attack paths return `False`.

---

### TC-09: FastAPI HTTP Endpoints Contract Verification
- **Objective**: Verify HTTP status codes, templates, and JSON response schemas via `TestClient`.
- **Execution Steps**:
  1. Send `GET /` -> verify status 200 and title in HTML.
  2. Send `GET /all-users` -> verify status 200.
  3. Send `GET /test-image?prompt=Cyberpunk_Hero` -> verify status 200 and `"path"` in JSON.
  4. Send `GET /download-pdf?file_path=../../etc/passwd` -> verify status 400 Bad Request.
- **Expected Result**: All status codes match specifications; path traversal attempt is rejected with HTTP 400.
