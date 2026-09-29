# 📝 Development Notes & Technical Log

## 1. Architectural Insights & Technical Decisions

### A. The Dual LLM Pipeline Strategy
During early prototyping, a single prompt was used to request both the structured 5-panel layout and the full character dialogue and narration. This approach caused two recurring failure modes:
1. LLMs occasionally corrupted the JSON structure when producing long, expressive dialogue with unescaped quotation marks.
2. The dialogue quality suffered because the model prioritized adhering to JSON syntax over rich creative narration.

**Solution Implemented**:
- Split into two sequential stages:
  - `gemini_flash.py`: Uses `gemini-1.5-flash` solely to generate a compact, strictly typed 5-panel JSON outline.
  - `gemini_pro.py`: Takes the parsed outline and tasks `gemini-1.5-pro` with writing expressive dialogue, ambient captions, and sound effects (*POW!*, *CRACK!*).

---

### B. Defensive Fallback Engineering
Cloud generative AI endpoints are subject to quota exhaustion (HTTP 429), API version deprecation, network latency spikes, or invalid keys. ComicCraft was architected so that **the user experience never breaks**:
- **Outline Generation**: If Gemini is unreachable or returns malformed JSON, `_generate_fallback_outline()` parses key story elements (hero name, setting, tone, style) using regex and produces a coherent 5-panel narrative arc.
- **Dialogue Scripting**: If the narrative model call fails, `_generate_fallback_story()` generates customized dialogue and action captions.
- **Illustration Pipeline**:
  - Tier 1: Attempts Google Imagen 3 diffusion model.
  - Tier 2: Attempts Gemini SVG vector illustration with ReportLab rasterization.
  - Tier 3: Engages our native procedural Pillow Comic Art Engine.

---

### C. Procedural Halftone Ben-Day Dot Engine (`image_generator.py`)
To ensure the fallback illustrations look like authentic retro comic panels rather than blank placeholders, we built a dedicated drawing engine using Pillow:
1. **Dynamic Celestial Gradients**: Calculates smooth vertical color interpolation based on environment keywords (`is_forest`, `is_cyber`, `is_space`).
2. **Ben-Day Halftone Dot Matrix**: Iterates over a two-dimensional grid (`step=18px`) drawing semi-transparent ellipses across the upper sky.
3. **Layered Terrain & Skylines**:
   - For Cyberpunk: Renders skyscraper silhouettes with glowing neon and warm yellow window grids.
   - For Space: Renders asteroid horizons and glowing cyan moons.
   - For Forest/Fantasy: Renders multi-tiered pine tree canopies and rolling hill contours.
4. **Hero Silhouette Art**: Draws a cape-wearing adventurer silhouette or animal hero with bold black ink outlines.
5. **Comic Framing & Inking**: Applies outer double black ink borders, action speed lines, and issue banner headers.

---

### D. Typography & Unicode Sanitization in PDF Export (`exporters.py`)
The `fpdf2` engine provides lightweight PDF compilation, but default fonts fail on non-Latin-1 typographical characters commonly produced by modern LLMs (e.g., curly quotes `“`, `”`, curly apostrophes `’`, em-dashes `—`, ellipses `…`).
- **Solution**: The `clean_text_for_pdf()` utility maps smart typographical characters to standard ASCII/Latin-1 equivalents before rendering.
- **Font Embedding**: The exporter automatically detects TrueType comic fonts (`comic.ttf`, `comicbd.ttf`) in `static/fonts/` and registers them dynamically with FPDF. If absent, it gracefully falls back to Helvetica.

---

### E. Security Hardening
- **Path Traversal Protection**: On the `/download-pdf` route, the incoming `file_path` parameter is normalized with `os.path.normpath` and strictly checked against `static/exports/`. Any attempt to escape the export directory is rejected with an HTTP 400 Bad Request.
- **Secret Isolation**: The `.env` file containing `GEMINI_API_KEY` is strictly excluded from version control via `.gitignore`.
