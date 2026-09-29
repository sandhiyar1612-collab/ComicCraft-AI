import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    import google.generativeai as genai
except ImportError:
    genai = None

def get_gemini_api_key():
    return os.getenv("GEMINI_API_KEY", "").strip()

def _generate_fallback_outline(user_prompt: str) -> list:
    """
    Fallback generator in case Gemini API key is missing or quota is exceeded.
    Generates a structured, engaging 5-panel comic storyline customized to the prompt.
    """
    # Extract details or use defaults
    char_match = re.search(r"main character is ([^.\n]+)", user_prompt, re.I)
    char_name = char_match.group(1).strip() if char_match else "The Hero"

    setting_match = re.search(r"setting is a? ([^.\n]+)", user_prompt, re.I)
    setting = setting_match.group(1).strip() if setting_match else "an enigmatic world"

    tone_match = re.search(r"tone is ([^.\n,]+)", user_prompt, re.I)
    tone = tone_match.group(1).strip() if tone_match else "dramatic"

    style_match = re.search(r"art style is ([^.\n]+)", user_prompt, re.I)
    style = style_match.group(1).strip() if style_match else "classic comic book"

    return [
        {
            "panel": 1,
            "title": f"The Journey Begins: {setting.title()}",
            "scene_description": f"{char_name} stands boldly at the threshold of {setting}, observant and filled with determination under cinematic lighting.",
            "image_prompt": f"Vintage comic book art style, {char_name} arriving at {setting}, dynamic low-angle composition, dramatic comic paper textures, bold ink outlines, halftone print, vivid colors"
        },
        {
            "panel": 2,
            "title": "A Mysterious Discovery",
            "scene_description": f"Deeper into the {setting}, an unexpected discovery reveals itself, sparking intrigue and a subtle hint of danger in a {tone} mood.",
            "image_prompt": f"Comic book panel illustration, {char_name} discovering a glowing ancient artifact or cryptic sign in {setting}, retro color palette, crisp line art, suspenseful lighting"
        },
        {
            "panel": 3,
            "title": "The Confrontation",
            "scene_description": f"Tension reaches its peak as a sudden challenge tests {char_name}'s courage and skill in an intense standoff.",
            "image_prompt": f"Dynamic action comic panel, {char_name} facing an intense challenge in {setting}, motion lines, bold comic action poses, saturated vintage comic colors, halftone dots"
        },
        {
            "panel": 4,
            "title": "Turning the Tide",
            "scene_description": f"With quick wit and unyielding resolve, {char_name} unleashes an ingenious strategy, transforming the battle into a turning point.",
            "image_prompt": f"High energy comic art, {char_name} pulling off a triumphant move or casting a brilliant effect in {setting}, explosive comic composition, vibrant pop art colors"
        },
        {
            "panel": 5,
            "title": "A Hero's Dawn",
            "scene_description": f"The dust settles over {setting}. {char_name} looks toward the horizon, victorious and ready for the next grand adventure.",
            "image_prompt": f"Cinematic comic book finale panel, {char_name} standing tall at sunset over {setting}, warm golden hour lighting, heroic silhouette, vintage newsprint comic texture"
        }
    ]

def generate_outline(user_prompt: str, api_key: str = None) -> list:
    """
    Generates a 5-panel comic layout based on the user's story idea using Gemini.
    
    Args:
        user_prompt (str): The user's comic idea prompt.
        api_key (str, optional): Gemini API key override.
        
    Returns:
        list: A list of dictionaries, one for each panel.
    """
    prompt = f"""You are a professional AI comic planner.

Your task is to generate a *strictly formatted* JSON array containing 5 panel descriptions for a comic based on the story idea below:

STORY: "{user_prompt}"

Each JSON object must include:
- "panel": (integer)
- "title": (string)
- "scene_description": (string)
- "image_prompt": (string)

Respond ONLY in this valid JSON format, without any explanations or markdown:
[
  {{
    "panel": 1,
    "title": "Title here",
    "scene_description": "Scene description here",
    "image_prompt": "Image prompt for Stable Diffusion"
  }}
]"""

    if not api_key:
        api_key = get_gemini_api_key()

    if not api_key or not genai:
        print("[NOTICE] GEMINI_API_KEY not configured or google-generativeai unavailable. Using intelligent comic fallback.")
        return _generate_fallback_outline(user_prompt)

    try:
        genai.configure(api_key=api_key)
        candidate_models = [
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-2.5-flash",
            "gemini-1.5-flash"
        ]

        output_text = None
        for model_name in candidate_models:
            try:
                print(f"[GEMINI FLASH] Attempting outline generation with model '{model_name}'...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and hasattr(response, "text") and response.text:
                    output_text = response.text.strip()
                    print(f"[GEMINI FLASH] Successfully generated outline with '{model_name}'!")
                    break
            except Exception as e_m:
                print(f"[GEMINI FLASH] Model '{model_name}' notice: {e_m}")
                continue

        if not output_text:
            print("[NOTICE] No candidate Gemini model succeeded. Using intelligent comic fallback.")
            return _generate_fallback_outline(user_prompt)

        # Remove any markdown formatting if present
        if output_text.startswith("```json"):
            output_text = output_text.replace("```json", "").replace("```", "").strip()
        elif output_text.startswith("```"):
            output_text = output_text.replace("```", "").strip()

        # Extract json array if extra text is around it
        match = re.search(r"\[\s*\{.*\}\s*\]", output_text, re.DOTALL)
        if match:
            output_text = match.group(0)

        panel_data = json.loads(output_text)

        # Additional structure validation
        if not isinstance(panel_data, list) or len(panel_data) == 0:
            raise ValueError("Gemini response is not a valid list.")

        for panel in panel_data:
            if not isinstance(panel, dict) or not all(key in panel for key in ("panel", "title", "scene_description", "image_prompt")):
                raise ValueError(f"Invalid panel format or missing keys: {panel}")

        return panel_data

    except json.JSONDecodeError as e:
        print("[ERROR] JSON Decode Error:", e)
        print("[ERROR] Full Text Received:\n", locals().get("output_text", ""))
        return _generate_fallback_outline(user_prompt)
    except Exception as e:
        print("[WARNING] Gemini Flash generation notice:", e)
        print("Falling back to structured comic storyline generator.")
        return _generate_fallback_outline(user_prompt)

