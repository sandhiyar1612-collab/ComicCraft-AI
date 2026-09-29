# 👥 User Requirements Specification

## 1. User Personas

### Persona A: Maya — Indie Writer & Comic Enthusiast
- **Background**: Writes short fantasy stories; has vivid visual concepts but cannot draw human figures or perspective.
- **Goal**: Quickly turn a story concept into a 5-panel comic strip with atmospheric dialogue and download it as a comic PDF to share with friends.
- **Pain Point**: Cannot afford $300-$500 per page for freelance illustrators; Midjourney requires hours of complex prompt engineering and doesn't output speech bubbles or PDFs.

### Persona B: David — High School Science & History Teacher
- **Background**: Wants to make lesson topics (e.g. discovery of penicillin, voyage to Mars) exciting for students.
- **Goal**: Create engaging, educational visual stories in minutes with zero software setup.
- **Pain Point**: Lacks graphic design software skills and has very limited prep time between classes.

### Persona C: Rohit — Indie Game Developer & Storyboarder
- **Background**: Prototyping game narrative cutscenes and quest storyboards.
- **Goal**: Use automated scripts via REST API (`/generate-comic/json`) to create visual storyboard sequences for quest pitches.
- **Pain Point**: Manual sketching delays sprint cycles and game design document updates.

---

## 2. User Stories

| ID | User Story | Priority | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **US-01** | As a storyteller, I want to enter my plot idea, character name, setting, tone, and art style so that the AI can craft a custom comic strip. | **High** | System accepts the 5 parameters and generates a 5-panel sequential narrative. |
| **US-02** | As a first-time user, I want 1-click creative presets so that I can experience comic generation without typing complex prompts. | **Medium** | Clicking a preset button (e.g., "Cyberpunk", "Space", "Noir") automatically populates all form fields. |
| **US-03** | As a comic reader, I want to preview each panel in sequence with artwork, captions, and speech bubbles in an authentic comic layout. | **High** | `comic_preview.html` renders all 5 panels with vintage typography, borders, and comic cards. |
| **US-04** | As a creator, I want to download my complete comic as a multi-page PDF so that I can print or publish it. | **High** | Clicking "Download PDF" retrieves a properly formatted multi-page PDF with custom comic fonts. |
| **US-05** | As an archivist, I want to browse past comic issues in a vault gallery so that I can view and re-download previous creations. | **Medium** | The `/all-users` / `/gallery` page lists all previous PDF exports with timestamps and file sizes. |
| **US-06** | As a developer, I want to supply a Gemini API key via the browser interface or `.env` file so that I can use my own Google AI quota. | **High** | Keys can be saved via the UI key bar or configured in `.env`, with visual status indicator. |
| **US-07** | As an API consumer, I want a JSON endpoint to automate comic generation without web browser dependencies. | **High** | `POST /generate-comic/json` accepts JSON and returns panel metadata and PDF path. |
