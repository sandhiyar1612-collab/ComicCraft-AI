# 📡 REST API Documentation

ComicCraft provides both interactive HTML web endpoints and headless JSON REST endpoints for automated integrations, mobile clients, and developer tools.

- **Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Specification**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Endpoint Summary Table

| Method | Endpoint | Description | Request Format | Response Format |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Web Comic Studio Homepage | None | HTML |
| `POST` | `/generate` | Web Form Comic Generation | Form Data | HTML |
| `POST` | `/generate-comic/json` | Headless Comic Generation | JSON (`PromptRequest`) | JSON (`ComicResponse`) |
| `POST` | `/api/save-key` | In-Browser Gemini Key Setup | JSON (`{"api_key": "..."}`) | JSON (`{"status": "..."}`) |
| `GET` | `/all-users` | Comic Vault Archive Gallery | None | HTML |
| `GET` | `/gallery` | Alias for Comic Vault Archive | None | HTML |
| `GET` | `/download-pdf` | Secure Direct PDF Download | Query Param (`file_path`) | Binary (`application/pdf`) |
| `GET` | `/export-success` | Download Celebration Page | Query Param (`pdf_path`) | HTML |
| `GET` | `/test-image` | Developer Image Engine Test | Query Param (`prompt`) | JSON |

---

## Endpoint Details

### 1. Headless Comic Generation: `POST /generate-comic/json`
Generates a complete 5-panel comic storyline, artwork, and PDF archive asynchronously.

- **Headers**: `Content-Type: application/json`
- **Request Body (`PromptRequest`)**:
```json
{
  "prompt": "A courageous cyborg ninja infiltrating a high-security neon pagoda",
  "character_name": "Ryu-7",
  "setting": "Neo Kyoto Rooftops",
  "tone": "Action-Packed & Dramatic",
  "style": "Cyberpunk Anime Comic"
}
```

- **Response (HTTP 200 OK)**:
```json
{
  "status": "success",
  "layout": [
    {
      "panel": 1,
      "title": "The Journey Begins: Neo Kyoto Rooftops",
      "image_path": "static/panels/panel_Vintage_comic_075f1178_831619.png",
      "text": "**CAPTION:** Rain slickers across the steel rooftops.\n**NARRATION:** Ryu-7 approaches the target perimeter.\nRYU-7: \"Initiating optical camouflage... now!\"",
      "scene_description": "Ryu-7 perches on an antenna spire looking down at the neon pagoda.",
      "image_prompt": "Vintage comic book art style, Ryu-7 arriving at Neo Kyoto Rooftops..."
    }
  ],
  "pdf_path": "/static/exports/comic_20260928115817.pdf"
}
```

- **Example cURL Command**:
```bash
curl -X POST "http://127.0.0.1:8000/generate-comic/json" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "A brave red fox exploring an enchanted glowing forest",
       "character_name": "Rusty",
       "setting": "Whispering Pines",
       "tone": "Wonder",
       "style": "Classic Comic Book"
     }'
```

---

### 2. Save Gemini Key: `POST /api/save-key`
Saves and persists a Gemini API key into the environment and `.env` file.

- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "api_key": "AIzaSyD-sample_gemini_api_key_here"
}
```
- **Response (HTTP 200 OK)**:
```json
{
  "status": "success",
  "message": "Gemini API Key saved successfully!"
}
```

---

### 3. Secure PDF Download: `GET /download-pdf`
Streams the compiled comic PDF file for direct local saving.

- **Query Parameters**:
  - `file_path` (required): Relative path to the PDF (e.g., `static/exports/comic_20260928115817.pdf`).
- **Security Check**: The file path must be verified within `static/exports/`. Attempted directory traversal returns HTTP 400.
- **Response (HTTP 200 OK)**: Binary stream with `Content-Type: application/pdf` and `Content-Disposition: attachment; filename="comic_...pdf"`.

---

### 4. Developer Test Image: `GET /test-image`
Utility route to independently verify the illustration pipeline.

- **Query Parameters**: `prompt` (string, optional)
- **Response (HTTP 200 OK)**:
```json
{
  "message": "Image generated successfully",
  "path": "/static/panels/panel_Cyberpunk_Hero_8c4b7583_454350.png"
}
```
