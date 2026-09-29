"""
ComicCraft Source Main Application Entry Point
"""
import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Ensure repository root is on sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.routes import router

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate personalized comic book stories, illustrations, and PDFs using AI models",
    version="1.0.0"
)

# Ensure required static directories exist
for folder in ["static", "static/panels", "static/exports", "static/fonts", "static/css", "static/img"]:
    os.makedirs(folder, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("05_Project_Development_Phase.source.main:app", host="127.0.0.1", port=8000, reload=True)
