"""
Pydantic Schemas for ComicCraft API Requests and Responses
"""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    """
    Schema for headless / automated comic generation requests.
    """
    prompt: str = Field(..., min_length=3, description="Main story premise or concept")
    character_name: str = Field(..., min_length=1, description="Protagonist name")
    setting: str = Field(..., min_length=2, description="Location or world setting")
    tone: str = Field(..., description="Story mood (e.g., dramatic, funny, noir, epic)")
    style: str = Field(..., description="Visual art style (e.g., classic comic book, anime, realistic)")

class KeySaveRequest(BaseModel):
    """
    Schema for saving Gemini API key from browser.
    """
    api_key: str = Field(..., min_length=5, description="Google Gemini API Key")

class PanelSchema(BaseModel):
    """
    Schema representing a single compiled comic panel.
    """
    panel: int
    title: str
    image_path: str
    text: str
    scene_description: str
    image_prompt: str

class ComicResponse(BaseModel):
    """
    Schema for JSON comic generation response.
    """
    status: str = "success"
    layout: List[Dict[str, Any]]
    pdf_path: str
