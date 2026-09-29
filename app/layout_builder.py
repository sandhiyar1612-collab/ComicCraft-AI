import re

def build_comic_layout(image_paths: list, full_story: str, outline: list) -> list:
    """
    Organizes the generated images, panel outlines, and full comic story into a structured layout.
    
    Args:
        image_paths (list): List of file paths to generated panel images.
        full_story (str): Complete comic story text.
        outline (list): List of outline panel dictionaries.
        
    Returns:
        list: Structured list of comic panel dictionaries.
    """
    # Robust split on "**Panel" or "Panel [0-9]"
    raw_segments = re.split(r'(?i)(?=\*?\*?panel\s+\d+)', full_story)
    story_panels = [seg.strip() for seg in raw_segments if seg.strip()]

    # If splitting resulted in fewer items than outline, fall back to outline-based extraction
    if len(story_panels) < len(outline):
        story_panels = []
        for i, panel_info in enumerate(outline, start=1):
            title = panel_info.get("title", f"Panel {i}") if isinstance(panel_info, dict) else f"Panel {i}"
            desc = panel_info.get("scene_description", "") if isinstance(panel_info, dict) else str(panel_info)
            story_panels.append(
                f"**Panel {i}: {title}**\n**CAPTION:** Whispers echo across the scene.\n**NARRATION:** {desc}"
            )

    layout = []
    for idx, (image, text, panel_info) in enumerate(zip(image_paths, story_panels, outline), start=1):
        # Extract title from panel_info if dict
        title = panel_info.get("title", f"Panel {idx}") if isinstance(panel_info, dict) else f"Panel {idx}"
        scene_desc = panel_info.get("scene_description", "") if isinstance(panel_info, dict) else ""
        image_prompt = panel_info.get("image_prompt", "") if isinstance(panel_info, dict) else ""

        # Remove header/title line like "**Panel 1: Title**" from text body
        lines = text.strip().splitlines()
        if lines and ("panel" in lines[0].lower() or lines[0].startswith("**")):
            cleaned_text = "\n".join(lines[1:]).strip()
        else:
            cleaned_text = text.strip()

        # If text is empty, provide default narration
        if not cleaned_text:
            cleaned_text = f"**NARRATION:** {scene_desc}"

        layout.append({
            "panel": idx,
            "title": title,
            "image_path": image,
            "text": cleaned_text,
            "scene_description": scene_desc,
            "image_prompt": image_prompt
        })

    return layout
