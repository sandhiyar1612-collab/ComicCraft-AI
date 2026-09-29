import os
import traceback
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class PromptRequest(BaseModel):
    prompt: str = Field(..., description="Main story prompt")
    character_name: str = Field(..., description="Main character name")
    setting: str = Field(..., description="Setting or location")
    tone: str = Field(..., description="Story tone (e.g. dramatic, funny, poetic)")
    style: str = Field(..., description="Art style (e.g. comic book, anime, realistic)")

def save_api_key_to_env(key: str):
    """Persists API key to .env file and process environment."""
    os.environ["GEMINI_API_KEY"] = key
    env_path = ".env"
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    key_found = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("GEMINI_API_KEY="):
            new_lines.append(f"GEMINI_API_KEY={key}\n")
            key_found = True
        else:
            new_lines.append(line)
    if not key_found:
        new_lines.insert(0, f"GEMINI_API_KEY={key}\n")
    with open(env_path, "w") as f:
        f.writelines(new_lines)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Renders the ComicCraft homepage where users can enter their comic parameters.
    """
    current_key = os.getenv("GEMINI_API_KEY", "").strip()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"gemini_key": current_key}
    )

@router.post("/api/save-key")
async def save_key(payload: dict):
    """API endpoint to quickly save Gemini API key from the browser."""
    api_key = payload.get("api_key", "").strip()
    if api_key:
        save_api_key_to_env(api_key)
        return {"status": "success", "message": "Gemini API Key saved successfully!"}
    return {"status": "error", "message": "API key cannot be empty"}

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...),
    gemini_api_key: str = Form(None)
):
    """
    Handles form submission from the index page, orchestrates outline generation,
    story writing, image creation, layout compilation, and PDF export.
    """
    try:
        # Check if an API key was passed in form
        active_key = (gemini_api_key or "").strip()
        if not active_key:
            active_key = os.getenv("GEMINI_API_KEY", "").strip()
        elif active_key and active_key != os.getenv("GEMINI_API_KEY", "").strip():
            save_api_key_to_env(active_key)

        # Combine user inputs into single full prompt as required by project spec
        full_prompt = (
            f"{prompt}\n"
            f"The main character is {character_name}.\n"
            f"The setting is a {setting}.\n"
            f"The tone is {tone}. The art style is {style}."
        )

        # Step 1: Generate panel outline
        outline = generate_outline(full_prompt, api_key=active_key)
        if not isinstance(outline, list) or not all("image_prompt" in panel for panel in outline if isinstance(panel, dict)):
            from app.gemini_flash import _generate_fallback_outline
            outline = _generate_fallback_outline(full_prompt)

        # Step 2: Generate story
        full_story = generate_story(outline, api_key=active_key)

        # Step 3: Generate images for each panel
        images = [
            generate_image(panel.get("image_prompt", prompt), api_key=active_key)
            for panel in outline
        ]

        # Step 4: Build comic layout
        layout = build_comic_layout(images, full_story, outline)

        # Step 5: Export to PDF
        pdf_path = save_pdf(layout)
        web_pdf_path = "/" + pdf_path.replace("\\", "/")

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "layout": layout,
                "pdf_path": web_pdf_path,
                "story_prompt": prompt,
                "character_name": character_name,
                "setting": setting,
                "tone": tone,
                "style": style
            }
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    """
    JSON API endpoint for headless or automated comic generation.
    """
    try:
        full_prompt = (
            f"{payload.prompt}\n"
            f"The main character is {payload.character_name}.\n"
            f"The setting is a {payload.setting}.\n"
            f"The tone is {payload.tone}. The art style is {payload.style}."
        )

        outline = generate_outline(full_prompt)
        if not isinstance(outline, list) or not all("image_prompt" in panel for panel in outline if isinstance(panel, dict)):
            from app.gemini_flash import _generate_fallback_outline
            outline = _generate_fallback_outline(full_prompt)
        full_story = generate_story(outline)
        images = [generate_image(panel.get("image_prompt", payload.prompt)) for panel in outline]
        layout = build_comic_layout(images, full_story, outline)
        pdf_path = save_pdf(layout)
        web_pdf_path = "/" + pdf_path.replace("\\", "/")

        return {
            "status": "success",
            "layout": layout,
            "pdf_path": web_pdf_path
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str):
    """
    Renders confirmation page after comic download.
    """
    # Ensure proper web formatting
    clean_web_path = "/" + pdf_path.lstrip("/").replace("\\", "/")
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": clean_web_path}
    )

@router.get("/test-image")
async def test_image(prompt: str = "A futuristic city at sunset, sci-fi, cinematic, artstation"):
    """
    Developer utility route to test image generation functionality separately.
    """
    try:
        image_path = generate_image(prompt)
        web_path = "/" + image_path.replace("\\", "/")
        return {
            "message": "Image generated successfully",
            "path": web_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all-users", response_class=HTMLResponse)
@router.get("/gallery", response_class=HTMLResponse)
async def all_users(request: Request):
    """
    Renders the archive/gallery page listing all generated comics.
    """
    import glob
    from datetime import datetime

    export_files = glob.glob(os.path.join("static", "exports", "*.pdf"))
    comics = []
    for f in sorted(export_files, key=os.path.getmtime, reverse=True):
        stat = os.stat(f)
        created_dt = datetime.fromtimestamp(stat.st_mtime).strftime("%b %d, %Y %I:%M %p")
        web_path = "/" + f.replace("\\", "/")
        comics.append({
            "filename": os.path.basename(f),
            "path": web_path,
            "created_at": created_dt,
            "size_kb": round(stat.st_size / 1024, 1)
        })

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"comics": comics}
    )

@router.get("/download-pdf")
async def download_pdf(file_path: str):
    """
    Direct file download handler for exported PDF.
    """
    # Security check: must reside in static/exports
    normalized_path = os.path.normpath(file_path.lstrip("/"))
    if not normalized_path.startswith(os.path.normpath("static/exports")):
        raise HTTPException(status_code=400, detail="Invalid file path")
    
    if not os.path.exists(normalized_path):
        raise HTTPException(status_code=404, detail="PDF not found")

    filename = os.path.basename(normalized_path)
    return FileResponse(
        path=normalized_path,
        media_type="application/pdf",
        filename=filename
    )
