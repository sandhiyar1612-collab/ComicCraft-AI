import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate personalized comic book stories, illustrations, and PDFs using AI models",
    version="1.0.0"
)

# Ensure required static directories exist
for folder in ["static", "static/panels", "static/exports", "static/fonts", "static/css", "static/img"]:
    os.makedirs(folder, exist_ok=True)

# Mount static files for images, css, exports, and fonts
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include comic application routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    load_dotenv()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
