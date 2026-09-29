import os
import re
from datetime import datetime
from fpdf import FPDF

EXPORT_FOLDER = os.path.join("static", "exports")
os.makedirs(EXPORT_FOLDER, exist_ok=True)

FONT_REGULAR = os.path.join("static", "fonts", "comic.ttf")
FONT_BOLD = os.path.join("static", "fonts", "comicbd.ttf")

def clean_text_for_pdf(text: str) -> str:
    """
    Sanitizes string for safe rendering across PDF engines.
    Replaces special unicode characters with Latin-1 equivalents.
    """
    replacements = {
        '“': '"', '”': '"', '’': "'", '‘': "'", '—': '-', '–': '-',
        '…': '...', '•': '*', 'é': 'e', 'è': 'e', 'ê': 'e', 'á': 'a',
        'à': 'a', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n', 'ü': 'u'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Remove unsupported characters
    return text.encode('latin-1', 'replace').decode('latin-1')

def save_pdf(layout: list) -> str:
    """
    Compiles the full comic into a multi-page PDF file using FPDF.
    Each panel's image and narration are placed neatly on separate pages.
    
    Args:
        layout (list): List of panel layout dictionaries.
        
    Returns:
        str: Relative path to the generated PDF.
    """
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)

    has_comic_font = os.path.exists(FONT_REGULAR)
    if has_comic_font:
        try:
            pdf.add_font('ComicFont', '', FONT_REGULAR)
            if os.path.exists(FONT_BOLD):
                pdf.add_font('ComicFont', 'B', FONT_BOLD)
            font_family = 'ComicFont'
        except Exception as e:
            print(f"Font loading error, using Helvetica: {e}")
            font_family = 'Helvetica'
    else:
        font_family = 'Helvetica'

    for panel in layout:
        panel_num = panel.get("panel", 1)
        title = clean_text_for_pdf(panel.get("title", f"Panel {panel_num}"))
        image_path = panel.get("image_path", "")
        story_text = clean_text_for_pdf(panel.get("text", ""))
        scene_desc = clean_text_for_pdf(panel.get("scene_description", ""))

        pdf.add_page()

        # Vintage comic page background frame (Double Ink Border)
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.8)
        pdf.rect(8, 8, pdf.w - 16, pdf.h - 16)
        pdf.set_line_width(0.3)
        pdf.rect(10, 10, pdf.w - 20, pdf.h - 20)

        # Comic Banner Header
        pdf.set_fill_color(255, 230, 0) # Comic Yellow
        pdf.rect(12, 12, pdf.w - 24, 14, 'DF')
        
        pdf.set_font(font_family, 'B' if has_comic_font else '', 13)
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(12, 14)
        pdf.cell(pdf.w - 24, 10, f"COMICCRAFT  -  PANEL {panel_num}: {title.upper()}", align="C")

        # Comic Illustration
        y_image = 32
        image_height = 110
        image_width = pdf.w - 30

        if os.path.exists(image_path):
            try:
                # Black ink frame around image
                pdf.set_line_width(0.6)
                pdf.rect(14.5, y_image - 0.5, image_width + 1, image_height + 1)
                pdf.image(image_path, x=15, y=y_image, w=image_width, h=image_height)
            except Exception as e:
                pdf.set_xy(15, y_image)
                pdf.set_font(font_family, '', 10)
                pdf.multi_cell(image_width, 8, f"Image Preview: {image_path}")
        else:
            pdf.set_xy(15, y_image)
            pdf.set_font(font_family, '', 10)
            pdf.multi_cell(image_width, 8, f"[Illustration for Panel {panel_num}: {scene_desc}]")

        # Text Placement Below Image
        y_text = y_image + image_height + 8
        pdf.set_xy(15, y_text)

        # Scene description caption box
        if scene_desc:
            pdf.set_font(font_family, '', 9)
            pdf.set_fill_color(248, 243, 224) # Warm paper box
            pdf.set_draw_color(50, 50, 50)
            pdf.set_text_color(80, 80, 80)
            pdf.multi_cell(pdf.w - 30, 5, f"Scene: {scene_desc}", border=1, fill=True)
            y_text = pdf.get_y() + 4
            pdf.set_xy(15, y_text)

        # Story narration & dialogue
        pdf.set_font(font_family, '', 10)
        pdf.set_text_color(20, 20, 20)

        # Filter out repetitive title line
        story_lines = story_text.strip().splitlines()
        filtered_lines = []
        for line in story_lines:
            line_str = line.strip()
            if line_str.lower().startswith("**panel") or line_str.lower().startswith("panel"):
                continue
            # Clean bold markers for neat PDF output
            cleaned_line = line_str.replace("**", "").replace("*", "")
            filtered_lines.append(cleaned_line)

        cleaned_text = "\n".join(filtered_lines).strip()
        pdf.multi_cell(pdf.w - 30, 6, cleaned_text if cleaned_text else story_text)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)
    return pdf_path
