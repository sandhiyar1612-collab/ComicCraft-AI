# 🐛 Bug Reports & Defect Resolution Log

## Defect Summary Table

| Defect ID | Severity | Component | Summary | Resolution Status |
| :--- | :--- | :--- | :--- | :--- |
| **BUG-01** | High | `app.image_generator` | Imagen 3 API restriction in Developer mode causes 404 | **Resolved** (Cascading Fallback) |
| **BUG-02** | Medium | `app.gemini_flash` | Markdown code fence wrapping in LLM JSON output | **Resolved** (Regex & Fence Strip) |
| **BUG-03** | High | `app.exporters` | FPDF2 crash on typographic unicode quotes/dashes | **Resolved** (Latin-1 Translation) |
| **BUG-04** | Critical | `app.routes` | Potential path traversal vulnerability in `/download-pdf` | **Resolved** (Strict Path Normalization) |
| **BUG-05** | Medium | `app.exporters` | Missing TTF comic font error on minimal OS environments | **Resolved** (Helvetica Fallback) |
| **BUG-06** | Low | `06_.../test_suite.py`| Python `SyntaxError` importing module starting with number | **Resolved** (`importlib.import_module`) |

---

## Detailed Bug Reports

### BUG-01: Imagen 3 API Developer Mode Restriction
- **Discovered**: During cloud visual generation testing.
- **Root Cause**: The Google GenAI SDK `generate_images` method threw `ExperimentalWarning` and indicated that direct diffusion calls are restricted to Enterprise Agent Platform mode, returning 404 in Developer API keys.
- **Impact**: Image generation would halt or crash if relying solely on Imagen 3.
- **Resolution**: Implemented a defensive multi-tiered failover in `image_generator.py`:
  1. Try Imagen 3.
  2. If unavailable, try Gemini SVG generation.
  3. If unavailable, trigger the native Pillow Procedural Comic Art Engine, producing authentic 768x512 Ben-Day halftone scene illustrations in milliseconds.

---

### BUG-02: Markdown Code Fence Wrapping in Gemini JSON Response
- **Discovered**: During JSON outline generation parsing.
- **Root Cause**: LLMs frequently wrap JSON responses in markdown fences (```` ```json [ ... ] ``` ````), which causes standard `json.loads()` to raise `JSONDecodeError`.
- **Resolution**: In `gemini_flash.py`:
  ```python
  if output_text.startswith("```json"):
      output_text = output_text.replace("```json", "").replace("```", "").strip()
  elif output_text.startswith("```"):
      output_text = output_text.replace("```", "").strip()

  match = re.search(r"\[\s*\{.*\}\s*\]", output_text, re.DOTALL)
  if match:
      output_text = match.group(0)
  ```

---

### BUG-03: FPDF2 Unicode Latin-1 Character Crash
- **Discovered**: During PDF export with creative narration containing smart quotes (`“`, `”`) and em-dashes (`—`).
- **Root Cause**: Core PDF standard fonts use `latin-1` character sets; encountering raw UTF-8 quotation characters causes encoding exceptions.
- **Resolution**: Created `clean_text_for_pdf()` in `exporters.py`:
  ```python
  replacements = {
      '“': '"', '”': '"', '’': "'", '‘': "'", '—': '-', '–': '-',
      '…': '...', '•': '*', 'é': 'e', 'è': 'e'
  }
  for old, new in replacements.items():
      text = text.replace(old, new)
  return text.encode('latin-1', 'replace').decode('latin-1')
  ```

---

### BUG-04: Directory Traversal in PDF Download Handler
- **Discovered**: During security code review of `/download-pdf?file_path=...`.
- **Root Cause**: Unsanitized query parameters could allow attackers to traverse directories (e.g. `../../etc/passwd`).
- **Resolution**: Implemented strict canonical path verification in `routes.py` and `StorageManager.is_safe_export_path()`:
  ```python
  normalized_path = os.path.normpath(file_path.lstrip("/\\"))
  if not normalized_path.startswith(os.path.normpath("static/exports")):
      raise HTTPException(status_code=400, detail="Invalid file path: Security violation")
  ```

---

### BUG-05: Missing TTF Comic Font Error on Minimal Environments
- **Discovered**: In clean environments lacking TrueType font files.
- **Root Cause**: `fpdf.add_font()` raises `FileNotFoundError` if `comic.ttf` is missing.
- **Resolution**: Wrapped font loading in `os.path.exists()` check. If fonts are missing, the exporter automatically uses standard `Helvetica` with identical layout coordinates.
