# 🔄 Data Flow Specification

## 1. End-to-End Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Browser
    participant Routes as app.routes
    participant Flash as app.gemini_flash
    participant Pro as app.gemini_pro
    participant ImgGen as app.image_generator
    participant Layout as app.layout_builder
    participant PDF as app.exporters
    participant Disk as Local Filesystem

    User->>Routes: POST /generate (form data)
    Note over Routes: Combines prompt, character, setting, tone, style
    
    Routes->>Flash: generate_outline(full_prompt)
    alt Gemini Flash Success
        Flash-->>Routes: 5-panel outline JSON [panel, title, scene_desc, image_prompt]
    else API Quota / Missing Key
        Flash->>Flash: _generate_fallback_outline(full_prompt)
        Flash-->>Routes: Fallback 5-panel outline JSON
    end

    Routes->>Pro: generate_story(outline)
    alt Gemini Pro Success
        Pro-->>Routes: Detailed comic script (captions, dialogues, SFX)
    else API Quota / Missing Key
        Pro->>Pro: _generate_fallback_story(outline)
        Pro-->>Routes: Fallback comic script
    end

    loop For each panel (1 to 5)
        Routes->>ImgGen: generate_image(image_prompt)
        alt Imagen 3 API Available
            ImgGen->>Disk: Save PNG to static/panels/
        else Gemini SVG Available
            ImgGen->>Disk: Render SVG & rasterize to PNG
        else Offline / Quota Fallback
            ImgGen->>ImgGen: _draw_comic_scenic_image(prompt)
            ImgGen->>Disk: Save Scenic Halftone PNG to static/panels/
        end
        ImgGen-->>Routes: Filepath (static/panels/panel_*.png)
    end

    Routes->>Layout: build_comic_layout(images, full_story, outline)
    Note over Layout: RegEx splits narrative into panels,<br/>binds titles, prompts & images
    Layout-->>Routes: Structured layout list

    Routes->>PDF: save_pdf(layout)
    PDF->>Disk: Load comic fonts (static/fonts/comic.ttf)
    PDF->>Disk: Write multi-page A4 PDF to static/exports/comic_*.pdf
    PDF-->>Routes: pdf_path

    Routes-->>User: Render comic_preview.html (layout, pdf_path)
    User->>Routes: GET /download-pdf?file_path=...
    Routes->>Disk: Verify path security & read PDF
    Routes-->>User: FileResponse (application/pdf)
```

---

## 2. Data Transformation States

### State 1: Raw Ingestion Payload
```json
{
  "prompt": "A brave red fox exploring an enchanted glowing forest",
  "character_name": "Rusty the Fox",
  "setting": "Ancient Whispering Woods",
  "tone": "Wonder and Mystery",
  "style": "Vintage Halftone Comic Book"
}
```

### State 2: Aggregated Master Prompt
```text
A brave red fox exploring an enchanted glowing forest
The main character is Rusty the Fox.
The setting is a Ancient Whispering Woods.
The tone is Wonder and Mystery. The art style is Vintage Halftone Comic Book.
```

### State 3: Outline Representation (`generate_outline`)
```json
[
  {
    "panel": 1,
    "title": "The Journey Begins: Ancient Whispering Woods",
    "scene_description": "Rusty the Fox stands boldly at the threshold...",
    "image_prompt": "Vintage comic book art style, Rusty the Fox arriving at Ancient Whispering Woods..."
  },
  ... (5 items)
]
```

### State 4: Story Script Output (`generate_story`)
```text
**Panel 1: The Journey Begins: Ancient Whispering Woods**
**CAPTION:** The wind howls as our tale unfolds under uncharted skies.
**NARRATION:** Standing at the frontier, determination gleams in every motion.
RUSTY: "No matter what lies ahead, there's no turning back now!"
```

### State 5: Layout Dictionary (`build_comic_layout`)
```json
[
  {
    "panel": 1,
    "title": "The Journey Begins: Ancient Whispering Woods",
    "image_path": "static/panels/panel_Vintage_comic_075f1178_831619.png",
    "text": "**CAPTION:** The wind howls as our tale unfolds...\n**NARRATION:** Standing at the frontier...\nRUSTY: \"No matter what lies ahead...\"",
    "scene_description": "Rusty the Fox stands boldly at the threshold...",
    "image_prompt": "Vintage comic book art style..."
  },
  ... (5 items)
]
```

### State 6: Compiled Document (`save_pdf`)
- Destination: `static/exports/comic_20260928115817.pdf`
- Format: ISO 32000-1 (PDF) document with embedded TTF font streams and high-resolution PNG raster graphics.
