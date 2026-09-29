# 🚀 Proposed Solution Architecture

## 1. High-Level Concept
ComicCraft introduces an automated, asynchronous generative pipeline that breaks down the comic creation process into five discrete, deterministic stages orchestrated by a high-performance **FastAPI** backend:

```
[User Input] 
     │
     ▼
[Stage 1: Outline Generation (Gemini Flash)] ──► 5 Structured Panels (JSON)
     │
     ▼
[Stage 2: Script & Dialogue (Gemini Pro)]   ──► Captions, Narration, Dialogue (Text)
     │
     ▼
[Stage 3: Image Generation Engine]         ──► 5 Panel Illustrations (PNG)
     │
     ▼
[Stage 4: Layout Builder]                  ──► Unified Structured Comic Layout
     │
     ▼
[Stage 5: PDF Exporter (fpdf2)]            ──► Multi-Page Publication PDF
```

## 2. Technical Solution Pillars

### A. Dual LLM Pipeline for Precision & Depth
Rather than burdening a single prompt with story planning, dialogue writing, and visual prompt engineering simultaneously, ComicCraft splits the cognitive load:
- **`gemini-1.5-flash`**: Optimized for speed, low latency, and strict JSON compliance to produce the structural storyboard outline.
- **`gemini-1.5-pro`**: Leveraged for creative narrative depth, linguistic nuance, character voice differentiation, and comic onomatopoeia.

### B. Fail-Safe Multi-Tier Image Pipeline
Cloud generative APIs frequently encounter quota limits, rate throttling, network timeouts, or model deprecation. ComicCraft implements an active cascading fallback hierarchy:
1. **Google Imagen 3 API** (via `google-genai` SDK and Google AI Studio REST).
2. **Gemini SVG Comic Vector Engine** (generating raw vector XML and converting via rasterization).
3. **Procedural Scenic Comic Engine** (built with `Pillow`): generates customized scenic comic art with sky color gradients, Ben-Day dot matrices, celestial bodies, terrain contours, hero silhouette character art, banner badges, and double ink borders.

### C. Standardized Document Layout & PDF Exporter
- Employs `fpdf2` with custom TrueType comic fonts (`comic.ttf`, `comicbd.ttf`).
- Automated text wrapping, dynamic cell sizing, Latin-1 unicode normalization, header yellow banners, and outer ink frames.
- Instant persistent storage in `static/exports/comic_{timestamp}.pdf`.

### D. Dual Interface Support (Web UI & REST API)
- **Web UI**: Authentic comic paper aesthetic with responsive forms, 1-click presets, real-time Gemini API key setup, and flipbook loading modal.
- **REST API**: Headless endpoint (`/generate-comic/json`) returning JSON schema for automated integrations, CLI tools, and mobile frontends.
