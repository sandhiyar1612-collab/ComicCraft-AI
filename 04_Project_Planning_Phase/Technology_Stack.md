# 🛠️ Technology Stack Evaluation & Architecture Matrix

## 1. Complete Technology Stack Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COMICCRAFT TECH STACK                           │
├─────────────────────┬────────────────────────┬─────────────────────────┤
│ Tier / Domain       │ Technology Selected    │ Version / Standard      │
├─────────────────────┼────────────────────────┼─────────────────────────┤
│ Programming Language│ Python                 │ 3.10+ (Tested on 3.12)  │
│ Web API Framework   │ FastAPI                │ >= 0.110.0              │
│ ASGI Web Server     │ Uvicorn                │ >= 0.28.0               │
│ Data Validation     │ Pydantic               │ >= 2.6.0                │
│ Templating Engine   │ Jinja2                 │ >= 3.1.3                │
│ Storyboard LLM      │ Google Gemini Flash    │ gemini-1.5-flash        │
│ Narrative / SFX LLM │ Google Gemini Pro      │ gemini-1.5-pro          │
│ Image Generation    │ Google Imagen 3        │ imagen-3.0-generate-002 │
│ Procedural Graphics │ Pillow (PIL)           │ >= 10.2.0               │
│ Document Publishing │ FPDF2                  │ >= 2.7.8                │
│ HTTP Client         │ Requests               │ >= 2.31.0               │
│ Environment Mgmt    │ python-dotenv          │ >= 1.0.1                │
│ Frontend Design     │ Custom Comic Paper CSS │ CSS3 & Halftone Ben-Day │
│ Typography          │ Google Fonts & TTF     │ Bangers, Comic Neue     │
│ Containerization    │ Docker & Compose       │ Docker 20.10+           │
└─────────────────────┴────────────────────────┴─────────────────────────┘
```

---

## 2. In-Depth Architectural Rationale

### Why FastAPI over Flask or Django?
1. **Asynchronous Throughput**: FastAPI natively handles `async/await`, allowing non-blocking I/O during long-running LLM and image generation HTTP calls.
2. **Automatic Swagger UI (`/docs`)**: Instant interactive OpenAPI documentation without writing separate Swagger YAML or Postman collections.
3. **Pydantic Validation**: Automatic parameter casting, strict schema error messages, and type safety for both form and JSON inputs.

### Why Google Gemini (Flash + Pro)?
1. **Cost and Speed**: `gemini-1.5-flash` offers sub-second inference and large context windows, making it ideal for rapid storyboard and outline generation.
2. **Creative Nuance**: `gemini-1.5-pro` excels at character voice consistency, comedic timing, and structured dialogue formatting.
3. **Structured JSON Compliance**: Gemini Flash reliably generates parseable JSON arrays for the 5 comic panels.

### Why Pillow Procedural Halftone Engine for Fallback?
1. **Zero External Latency**: Renders a rich 768x512 comic scene in ~15 milliseconds.
2. **Authentic Comic Feel**: Implements genuine Ben-Day halftone dot grids, sky gradients, mountain/cyber silhouettes, character art, action banners, and heavy ink borders.
3. **No GPU Requirement**: Operates with standard CPU instructions and minimal memory footprint.

### Why FPDF2 for PDF Export?
1. **No Headless Browser Bloat**: Tools like Puppeteer require a full 500MB Chromium download and consume heavy RAM. `fpdf2` runs directly inside Python with negligible overhead.
2. **Typography Precision**: Supports custom TrueType fonts (`comic.ttf`, `comicbd.ttf`) for authentic comic lettering and styling.
3. **Direct Millimeter Grid Layout**: Allows precise placement of ink frames, yellow title bars, scene captions, and dialogue boxes.
