# 📝 Brainstorming Notes & Architectural Trade-offs

## 1. Initial Brainstorming Sessions

### Focus Questions
- *How can we make comic generation accessible to users who cannot draw?*
  - Answer: Accept simple natural language parameters (Story Idea, Character Name, Setting, Tone, Art Style) and translate them into complete sequential comic scenes.
- *How many panels make the ideal single-sitting comic experience?*
  - Answer: **5 Panels**. 3 panels is too brief for an emotional arc; 10 panels takes too long to generate on a free tier API. 5 panels neatly follows the classic 5-act dramatic structure (Exposition, Rising Action, Climax, Falling Action, Resolution).
- *What visual style evokes the most nostalgia and joy?*
  - Answer: The classic American Silver/Bronze-age comic style — warm newsprint paper, Ben-Day halftone dots, action starbursts, Comic Code Authority stamps, and vibrant primary colors (Yellow, Cyan, Ink Black, Comic Red).

---

## 2. Key Architectural Decisions & Trade-Offs

| Decision Area | Option A (Considered) | Option B (Selected) | Rationale for Decision |
| :--- | :--- | :--- | :--- |
| **Backend Framework** | Django / Flask | **FastAPI** | FastAPI provides native async support, automatic OpenAPI/Swagger documentation, strict Pydantic data validation, and ultra-low latency overhead. |
| **LLM Orchestration** | Single unified prompt | **Dual-stage (Flash + Pro)** | A single prompt often sacrifices either JSON schema rigor or story quality. Splitting outline planning (Flash) and dialogue/narration (Pro) yields superior results. |
| **PDF Generation** | Headless Chrome (Puppeteer) | **`fpdf2` Python Engine** | Headless Chrome requires 500MB+ browser binaries, high RAM usage, and complex Docker setups. `fpdf2` runs purely in Python with millisecond rendering speed and low resource footprint. |
| **Styling Strategy** | Generic Bootstrap / Tailwind | **Custom Vanilla CSS Comic System** | Standard CSS frameworks look sterile and corporate. A dedicated 800-line vanilla CSS design system (`comic.css`) allows authentic halftone dots, offset shadows, and custom comic typography. |
| **Storage Architecture** | Relational DB (PostgreSQL) | **File-Based Store (Phase 1-2)** | Early versions prioritize zero-setup portability. Generated assets are indexed cleanly in `static/exports/` and `static/panels/`. Database integration is planned for future multi-tenant authentication. |
| **API Key Management** | Strict server environment variable only | **Hybrid (.env + In-Browser Form Key)** | Enables immediate out-of-the-box usage for users who wish to test their own Google AI Studio keys directly through the web UI without SSH or shell access. |

---

## 3. Resilience and Fallback Brainstorming
- **The Quota Problem**: What happens if the user's Gemini key runs out of tokens or is invalid?
  - *Solution*: Never show a raw crash stacktrace to users. Detect missing or rate-limited keys and trigger algorithmic storyline generation (`_generate_fallback_outline` & `_generate_fallback_story`) and procedural Ben-Day comic illustration rendering (`_draw_comic_scenic_image`).
- **Font Fallback**: What if system comic fonts are missing?
  - *Solution*: Automatically check for `static/fonts/comic.ttf` and fallback gracefully to standard PDF fonts (`Helvetica`).
