"""
Configuration and Environment Settings Module for ComicCraft
"""
import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class AppSettings(BaseModel):
    """
    Centralized configuration settings for the ComicCraft application.
    """
    app_title: str = "ComicCraft - AI Comic Story Creator"
    app_version: str = "1.0.0"
    app_description: str = "Generate personalized comic book stories, illustrations, and PDFs using AI models"

    # Host & Port
    host: str = Field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))

    # AI API Keys
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", "").strip())
    hf_api_key: str = Field(default_factory=lambda: os.getenv("HF_API_KEY", "").strip())

    # Static Directories
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    static_dir: str = "static"
    panels_dir: str = os.path.join("static", "panels")
    exports_dir: str = os.path.join("static", "exports")
    fonts_dir: str = os.path.join("static", "fonts")
    css_dir: str = os.path.join("static", "css")
    templates_dir: str = "templates"

    def ensure_directories(self):
        """Ensures all necessary asset directories exist on disk."""
        for folder in [
            self.static_dir,
            self.panels_dir,
            self.exports_dir,
            self.fonts_dir,
            self.css_dir,
            os.path.join(self.static_dir, "img")
        ]:
            os.makedirs(folder, exist_ok=True)

settings = AppSettings()
settings.ensure_directories()
