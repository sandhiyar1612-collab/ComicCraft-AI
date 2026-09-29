import os
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

def _generate_fallback_story(outline: list) -> str:
    """
    Fallback story generator when Gemini API is unavailable or quota is exceeded.
    Creates vivid comic dialogue and captions for each panel.
    """
    story_parts = []
    for idx, panel in enumerate(outline, start=1):
        if isinstance(panel, dict):
            title = panel.get("title", f"Panel {idx}")
            desc = panel.get("scene_description", "")
        else:
            title = f"Chapter {idx}"
            desc = str(panel)

        if idx == 1:
            caption = "The wind howls as our tale unfolds under uncharted skies."
            narration = f"Standing at the frontier, determination gleams in every motion. {desc}"
            dialogue = 'HERO: "No matter what lies ahead, there\'s no turning back now!"'
        elif idx == 2:
            caption = "Whispers carried across the air. Ancient secrets stir."
            narration = f"Every step unveils another piece of the puzzle. {desc}"
            dialogue = 'HERO: "Wait... did you hear that? Something is watching us."'
        elif idx == 3:
            caption = "CRACK! Lightning flares across the horizon!"
            narration = f"The moment of reckoning arrives faster than expected! {desc}"
            dialogue = 'RIVAL: "You think courage alone can see you through?!"\nHERO: "Courage and a little bit of comic genius!"'
        elif idx == 4:
            caption = "KRA-KOOM! Energy erupts in a blinding flash of color!"
            narration = f"Trusting instincts honed through adversity, the tide miraculously turns! {desc}"
            dialogue = 'HERO: "Now\'s our chance—all or nothing!"'
        else:
            caption = "Quiet returns to the land. A new dawn breaks."
            narration = f"Victory shines brightly as peace settles over the horizon. {desc}"
            dialogue = 'HERO: "We did it. But I know this is only the beginning of our legend!"'

        story_parts.append(
            f"**Panel {idx}: {title}**\n"
            f"**CAPTION:** {caption}\n"
            f"**NARRATION:** {narration}\n"
            f"{dialogue}\n"
        )

    return "\n\n".join(story_parts)

def generate_story(outline: list, api_key: str = None) -> str:
    """
    Generates a detailed comic story with narration and character dialogue
    from a list of comic panel outlines using Gemini 1.5 Pro.
    
    Args:
        outline (list): A list of panel dictionaries or strings representing each comic panel's idea.
        api_key (str, optional): Gemini API key override.
        
    Returns:
        str: The generated comic story text.
    """
    # Format the panel outline as a numbered list for clarity
    formatted_items = []
    for i, item in enumerate(outline):
        if isinstance(item, dict):
            t = item.get("title", f"Panel {i+1}")
            d = item.get("scene_description", "")
            formatted_items.append(f"{i+1}. {t} - {d}")
        else:
            formatted_items.append(f"{i+1}. {item}")

    formatted_outline = "\n".join(formatted_items)

    prompt = f"""You're a comic book writer.

Given the following panel breakdown, write a comic-style story with engaging narration and character dialogues for each panel.

Panel Outline:
{formatted_outline}

Guidelines:
- Use a fun and engaging tone, like an actual comic book.
- For each panel, start with:
  **Panel [number]: [Panel Title]**
  **CAPTION:** [Brief atmospheric sound or environment caption]
  **NARRATION:** [Action, thought, or story narration]
  [Character Name]: "[Dialogue]"
- Include sound effects (e.g. *BAM!*, *WHOOSH!*, *CRACK!*) where fitting.
- Keep each panel self-contained but part of a cohesive story.
"""

    if not api_key:
        api_key = get_gemini_api_key()

    if not api_key or not genai:
        print("[NOTICE] GEMINI_API_KEY not configured or google-generativeai unavailable. Using fallback comic story.")
        return _generate_fallback_story(outline)

    try:
        genai.configure(api_key=api_key)
        candidate_models = [
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-3.1-pro-preview",
            "gemini-pro-latest",
            "gemini-2.5-pro",
            "gemini-1.5-pro"
        ]

        text = None
        for model_name in candidate_models:
            try:
                print(f"[GEMINI PRO] Attempting story scripting with model '{model_name}'...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and hasattr(response, "text") and response.text:
                    text = response.text.strip()
                    print(f"[GEMINI PRO] Successfully generated story with '{model_name}'!")
                    break
            except Exception as e_m:
                print(f"[GEMINI PRO] Model '{model_name}' notice: {e_m}")
                continue

        if text:
            return text
        print("[NOTICE] No candidate Gemini Pro model returned text. Using fallback comic story.")
        return _generate_fallback_story(outline)
    except Exception as e:
        print("[ERROR] Error generating story with Gemini Pro:", str(e))
        return _generate_fallback_story(outline)
