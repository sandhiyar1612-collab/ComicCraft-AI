import os
import re
import math
import time
import base64
import hashlib
import requests
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

STATIC_PANELS_DIR = os.path.join("static", "panels")
os.makedirs(STATIC_PANELS_DIR, exist_ok=True)

def sanitize_filename(prompt: str) -> str:
    """
    Creates a safe and unique filename based on prompt and timestamp.
    """
    clean_prompt = re.sub(r'[^a-zA-Z0-9_\- ]', '', prompt).strip().replace(" ", "_")[:30]
    prompt_hash = hashlib.md5(prompt.encode('utf-8')).hexdigest()[:8]
    timestamp = int(time.time() * 1000) % 1000000
    return f"panel_{clean_prompt}_{prompt_hash}_{timestamp}.png"

_IMAGEN_UNAVAILABLE = False
_SVG_UNAVAILABLE = False

def generate_image_with_gemini_imagen(prompt: str, api_key: str, output_path: str) -> bool:
    """
    Generates high-resolution comic illustration using Google Gemini's Imagen 3 API.
    Supports both google-genai SDK and direct Google AI Studio REST endpoints.
    """
    global _IMAGEN_UNAVAILABLE
    if _IMAGEN_UNAVAILABLE or not api_key:
        return False

    enhanced_prompt = (
        f"Vintage comic book art style, graphic novel panel illustration, "
        f"bold ink outlines, halftone print texture, rich cinematic lighting: {prompt}"
    )

    # 1. Try google-genai SDK
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        for model_name in ["imagen-3.0-generate-002", "imagen-3.0-fast-generate-001"]:
            try:
                print(f"[GEMINI] Calling Imagen 3 model '{model_name}'...")
                result = client.models.generate_images(
                    model=model_name,
                    prompt=enhanced_prompt,
                    config=dict(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        aspect_ratio="3:2"
                    )
                )
                if result and result.generated_images:
                    img_bytes = result.generated_images[0].image.image_bytes
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    print(f"[GEMINI] Successfully generated panel with {model_name}!")
                    return True
            except Exception as em:
                print(f"[GEMINI] Notice for model {model_name}: {em}")
    except Exception as e_sdk:
        print(f"[GEMINI] SDK notice: {e_sdk}")

    # 2. Try Google AI Studio REST endpoint
    try:
        for model_name in ["imagen-3.0-generate-002", "imagen-3.0-fast-generate-001"]:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:predict?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "instances": [{"prompt": enhanced_prompt}],
                "parameters": {"sampleCount": 1, "aspectRatio": "3:2"}
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                predictions = data.get("predictions", [])
                if predictions and len(predictions) > 0:
                    b64_data = predictions[0].get("bytesBase64Encoded")
                    if b64_data:
                        with open(output_path, "wb") as f:
                            f.write(base64.b64decode(b64_data))
                        print(f"[GEMINI REST] Successfully generated panel with {model_name}!")
                        return True
            else:
                print(f"[GEMINI REST] {model_name} response status: {resp.status_code}")
    except Exception as e_rest:
        print(f"[GEMINI REST] Notice: {e_rest}")

    _IMAGEN_UNAVAILABLE = True
    return False

def generate_image_with_gemini_svg(prompt: str, api_key: str, output_path: str) -> bool:
    """
    If Imagen is not enabled on the user's project, asks Gemini LLM
    to generate an intricate comic book SVG illustration and rasterizes it.
    """
    global _SVG_UNAVAILABLE
    if _SVG_UNAVAILABLE or not api_key:
        return False

    svg_prompt = f"""You are a professional comic book illustrator.
Create a complete, detailed SVG illustration for this comic panel scene:
"{prompt}"

STRICT RULES:
1. Output ONLY valid, raw SVG code starting with <svg and ending with </svg>. No markdown formatting or extra text.
2. The SVG must have: viewBox="0 0 768 512" width="768" height="512" xmlns="http://www.w3.org/2000/svg".
3. Use a vibrant comic art style:
   - Dramatic sky gradient and sun/moon.
   - Background scenery (silhouettes of trees, hills, buildings, or stars).
   - Character silhouette or illustration in the center/foreground with bold black outline (stroke="#000" stroke-width="3").
   - Action speed lines or comic frame.
   - Rich colors (deep greens, warm golds, comic reds, or cyan blues).
"""
    try:
        import google.generativeai as genai
        text = ""
        for m_name in ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-flash-latest"]:
            try:
                model = genai.GenerativeModel(m_name)
                response = model.generate_content(svg_prompt)
                if response and hasattr(response, "text") and response.text:
                    text = response.text.strip()
                    break
            except Exception:
                continue
        
        # Clean markdown
        if "```xml" in text:
            text = text.split("```xml", 1)[1].split("```", 1)[0].strip()
        elif "```svg" in text:
            text = text.split("```svg", 1)[1].split("```", 1)[0].strip()
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0].strip()

        if "<svg" in text and "</svg>" in text:
            svg_content = text[text.find("<svg"):text.rfind("</svg>") + 6]
            svg_temp_path = output_path.replace(".png", ".svg")
            with open(svg_temp_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

            # Rasterize SVG to PNG using svglib & reportlab
            try:
                from svglib.svglib import svg2rlg
                from reportlab.graphics import renderPM
                drawing = svg2rlg(svg_temp_path)
                if drawing:
                    renderPM.drawToFile(drawing, output_path, fmt="PNG")
                    print("[GEMINI SVG] Successfully rendered Gemini comic SVG illustration to PNG!")
                    return True
            except Exception as e_raster:
                print(f"[GEMINI SVG] Rasterization notice: {e_raster}")
    except Exception as e_svg:
        print(f"[GEMINI SVG] Notice: {e_svg}")

    _SVG_UNAVAILABLE = True
    return False

def _draw_comic_scenic_image(prompt: str, output_path: str):
    """
    Renders an authentic, pictorial comic book scene using Pillow.
    Features layered landscapes, dynamic lighting, character silhouettes,
    halftone texture, and heavy ink borders.
    """
    width, height = 768, 512
    img = Image.new("RGB", (width, height), (250, 245, 230))
    draw = ImageDraw.Draw(img)
    lp = prompt.lower()

    is_forest = any(k in lp for k in ["forest", "tree", "wood", "nature", "jungle", "fox"])
    is_cyber = any(k in lp for k in ["cyber", "neon", "city", "tokyo", "tech", "robot"])
    is_space = any(k in lp for k in ["space", "star", "galaxy", "moon", "asteroid", "cat"])

    # 1. Sky Gradient
    sky_height = int(height * 0.65)
    for y in range(sky_height):
        ratio = y / sky_height
        if is_forest:
            r = int(255 * (1 - ratio * 0.25) + 60 * ratio * 0.25)
            g = int(220 * (1 - ratio * 0.35) + 130 * ratio * 0.35)
            b = int(140 * (1 - ratio * 0.50) + 190 * ratio * 0.50)
        elif is_cyber:
            r = int(20 * (1 - ratio) + 150 * ratio)
            g = int(10 * (1 - ratio) + 40 * ratio)
            b = int(60 * (1 - ratio) + 210 * ratio)
        elif is_space:
            r = int(10 * (1 - ratio) + 40 * ratio)
            g = int(12 * (1 - ratio) + 25 * ratio)
            b = int(45 * (1 - ratio) + 95 * ratio)
        else:
            r = int(255 * (1 - ratio * 0.2) + 90 * ratio * 0.2)
            g = int(210 * (1 - ratio * 0.3) + 140 * ratio * 0.3)
            b = int(120 * (1 - ratio * 0.4) + 200 * ratio * 0.4)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Celestial Body (Sun / Glowing Moon / Neon Sphere)
    cx_celestial = width // 2 + 80
    cy_celestial = 110
    if is_space or is_cyber:
        # Glowing Moon / Neon sphere
        draw.ellipse([cx_celestial - 55, cy_celestial - 55, cx_celestial + 55, cy_celestial + 55], fill=(0, 230, 255), outline=(0, 160, 220), width=3)
        draw.ellipse([cx_celestial - 40, cy_celestial - 40, cx_celestial + 40, cy_celestial + 40], fill=(240, 255, 255))
    else:
        # Golden Comic Sun
        draw.ellipse([cx_celestial - 60, cy_celestial - 60, cx_celestial + 60, cy_celestial + 60], fill=(255, 235, 110), outline=(240, 180, 40), width=4)
        draw.ellipse([cx_celestial - 45, cy_celestial - 45, cx_celestial + 45, cy_celestial + 45], fill=(255, 250, 190))

    # Halftone Dot Texture across sky
    for x in range(0, width, 18):
        for y in range(0, sky_height, 18):
            draw.ellipse([x, y, x + 2.5, y + 2.5], fill=(255, 255, 255, 60))

    # 3. Distant Mountains or City Skyline
    if is_cyber:
        # Futuristic Skyscraper Silhouettes
        for bx in range(0, width, 45):
            bh = 120 + ((bx * 31) % 150)
            by = height - bh - 80
            draw.rectangle([bx, by, bx + 40, height], fill=(18, 22, 38), outline=(0, 210, 255), width=2)
            # Glowing windows
            for wy in range(by + 15, height - 90, 22):
                draw.rectangle([bx + 8, wy, bx + 16, wy + 8], fill=(255, 230, 0))
                draw.rectangle([bx + 24, wy, bx + 32, wy + 8], fill=(0, 230, 255))
    elif is_space:
        # Cosmic Asteroid & Crater Horizon
        draw.polygon([(0, 310), (180, 260), (380, 290), (590, 250), (width, 300), (width, height), (0, height)], fill=(40, 35, 65), outline=(100, 90, 140), width=3)
    else:
        # Distant Blue Ridge Mountains
        draw.polygon([(0, 290), (180, 190), (360, 280), (550, 175), (width, 270), (width, height), (0, height)], fill=(100, 150, 130), outline=(60, 100, 85), width=3)

    # 4. Midground Scenery (Forest Trees / Terrain)
    if is_forest:
        for tx in range(0, width + 50, 36):
            th = 95 + ((tx * 23) % 65)
            ty = 310
            draw.polygon([(tx - 26, ty), (tx, ty - th), (tx + 26, ty)], fill=(32, 85, 52), outline=(12, 40, 20), width=2)

    # 5. Foreground Hill / Terrain
    terrain_color = (25, 75, 45) if is_forest else ((22, 28, 48) if is_cyber else (30, 25, 50))
    terrain_outline = (10, 30, 15) if is_forest else ((0, 210, 255) if is_cyber else (80, 70, 110))
    draw.ellipse([-120, 310, width + 120, 680], fill=terrain_color, outline=terrain_outline, width=5)

    # 6. Hero Character Silhouette
    cx_char = width // 2 - 40
    cy_char = 330

    if "fox" in lp or is_forest:
        # Beautiful Stylized Fox
        draw.ellipse([cx_char - 40, cy_char - 20, cx_char + 40, cy_char + 20], fill=(235, 95, 30), outline=(20, 20, 20), width=3)
        draw.polygon([(cx_char + 20, cy_char - 15), (cx_char + 65, cy_char - 10), (cx_char + 35, cy_char + 12)], fill=(245, 105, 35), outline=(20, 20, 20), width=2)
        draw.polygon([(cx_char + 28, cy_char - 15), (cx_char + 38, cy_char - 38), (cx_char + 48, cy_char - 12)], fill=(20, 20, 20))
        draw.polygon([(cx_char - 35, cy_char - 5), (cx_char - 85, cy_char - 35), (cx_char - 70, cy_char + 15)], fill=(235, 95, 30), outline=(20, 20, 20), width=3)
        draw.polygon([(cx_char - 70, cy_char - 25), (cx_char - 85, cy_char - 35), (cx_char - 75, cy_char - 5)], fill=(255, 255, 255))
        draw.line([(cx_char - 20, cy_char + 15), (cx_char - 25, cy_char + 52)], fill=(20, 20, 20), width=5)
        draw.line([(cx_char + 15, cy_char + 15), (cx_char + 20, cy_char + 52)], fill=(20, 20, 20), width=5)
        draw.ellipse([cx_char + 45, cy_char - 6, cx_char + 52, cy_char + 1], fill=(255, 255, 255))
        draw.ellipse([cx_char + 48, cy_char - 4, cx_char + 51, cy_char - 1], fill=(0, 0, 0))
    else:
        # Heroic Explorer / Adventurer Silhouette
        draw.ellipse([cx_char - 18, cy_char - 70, cx_char + 18, cy_char - 34], fill=(20, 20, 20)) # Head
        draw.polygon([(cx_char - 28, cy_char - 34), (cx_char + 28, cy_char - 34), (cx_char + 35, cy_char + 25), (cx_char - 35, cy_char + 25)], fill=(255, 42, 68), outline=(0, 0, 0), width=3) # Hero Cape
        draw.line([(cx_char - 14, cy_char + 25), (cx_char - 18, cy_char + 65)], fill=(20, 20, 20), width=6) # Left Leg
        draw.line([(cx_char + 14, cy_char + 25), (cx_char + 18, cy_char + 65)], fill=(20, 20, 20), width=6) # Right Leg

    # 7. Action Speed Lines in Corners
    for i in range(5):
        draw.line([(0, i * 16), (80 + i * 20, 0)], fill=(0, 0, 0), width=2)
        draw.line([(width, i * 16), (width - 80 - i * 20, 0)], fill=(0, 0, 0), width=2)

    # 8. Top Comic Badge Tag
    tag_text = "ENCHANTED FOREST" if is_forest else ("NEO TOKYO" if is_cyber else "DEEP COSMOS")
    draw.rectangle([width - 195, 18, width - 20, 48], fill=(255, 230, 0), outline=(0, 0, 0), width=2)
    try:
        font_sm = ImageFont.load_default(size=16)
        font_xs = ImageFont.load_default(size=14)
    except Exception:
        font_sm = ImageFont.load_default()
        font_xs = ImageFont.load_default()
    draw.text((width - 185, 23), f"★ {tag_text} ★", fill=(0, 0, 0), font=font_sm)

    # 9. Bottom Comic Scene Banner
    banner_y = height - 90
    draw.rectangle([20, banner_y, width - 20, height - 18], fill=(255, 252, 235), outline=(0, 0, 0), width=3)
    draw.rectangle([20, banner_y, 170, banner_y + 24], fill=(255, 42, 68), outline=(0, 0, 0), width=2)
    draw.text((32, banner_y + 4), "COMIC SCENE ART", fill=(255, 255, 255), font=font_xs)

    clean_p = prompt if len(prompt) < 110 else prompt[:107] + "..."
    draw.text((32, banner_y + 32), clean_p, fill=(20, 20, 20), font=font_xs)

    # 10. Heavy Ink Borders
    draw.rectangle([8, 8, width - 8, height - 8], outline=(0, 0, 0), width=6)
    draw.rectangle([12, 12, width - 12, height - 12], outline=(0, 0, 0), width=2)

    img.save(output_path, "PNG")

def generate_image(prompt: str, filename: str = None, api_key: str = None) -> str:
    """
    Generates a comic-style image based on prompt and saves to static/panels/.
    
    Generation Order:
    1. Google Gemini Imagen 3 (via api_key or GEMINI_API_KEY)
    2. Google Gemini SVG Comic Illustration Engine
    3. Procedural Scenic Comic Art Engine (with layered landscapes & character art)
    """
    if not filename:
        filename = sanitize_filename(prompt)

    if not filename.endswith(".png") and not filename.endswith(".jpg"):
        filename += ".png"

    path = os.path.join(STATIC_PANELS_DIR, filename)

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()

    # 1. Try Gemini Imagen 3
    if api_key and not _IMAGEN_UNAVAILABLE:
        print("[IMAGE_GEN] Attempting Gemini Imagen 3 generation with provided API key...")
        if generate_image_with_gemini_imagen(prompt, api_key, path):
            return path

    # 2. Try Gemini SVG Illustration
    if api_key and not _SVG_UNAVAILABLE:
        print("[IMAGE_GEN] Attempting Gemini Comic SVG generation...")
        if generate_image_with_gemini_svg(prompt, api_key, path):
            return path

    # 3. Scenic Comic Art Engine Fallback
    print("[IMAGE_GEN] Rendering pictorial comic scene illustration...")
    try:
        _draw_comic_scenic_image(prompt, path)
        return path
    except Exception as e:
        print(f"[ERROR] Comic scenic drawing failed: {e}")
        img = Image.new("RGB", (768, 512), color=(255, 240, 200))
        d = ImageDraw.Draw(img)
        d.text((50, 200), f"Comic Panel: {prompt[:80]}", fill=(0, 0, 0))
        img.save(path)
        return path
