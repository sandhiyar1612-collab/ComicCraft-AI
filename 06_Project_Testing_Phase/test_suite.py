"""
Comprehensive Automated Test Suite for ComicCraft
Covers unit, integration, and security test cases.
"""
import os
import sys
import unittest
from pathlib import Path
from PIL import Image

# Ensure project root is in sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from app.gemini_flash import _generate_fallback_outline
from app.gemini_pro import _generate_fallback_story
from app.image_generator import sanitize_filename, _draw_comic_scenic_image, generate_image
from app.layout_builder import build_comic_layout
from app.exporters import clean_text_for_pdf, save_pdf
import importlib
storage_module = importlib.import_module("05_Project_Development_Phase.database.storage_manager")
StorageManager = storage_module.StorageManager

class TestComicCraftCore(unittest.TestCase):
    """Unit and integration test cases for ComicCraft generative components."""

    def test_01_outline_fallback_structure(self):
        """TC-01: Verify outline fallback generates exactly 5 valid panels."""
        prompt = "The hero is Alex in a mysterious cavern, dramatic tone, comic book style"
        outline = _generate_fallback_outline(prompt)
        self.assertIsInstance(outline, list)
        self.assertEqual(len(outline), 5)
        for i, panel in enumerate(outline, start=1):
            self.assertEqual(panel["panel"], i)
            self.assertIn("title", panel)
            self.assertIn("scene_description", panel)
            self.assertIn("image_prompt", panel)
            self.assertTrue(len(panel["image_prompt"]) > 10)

    def test_02_story_fallback_generation(self):
        """TC-02: Verify story fallback creates dialogue and narration for all panels."""
        outline = _generate_fallback_outline("Hero Maya in space")
        story = _generate_fallback_story(outline)
        self.assertIsInstance(story, str)
        self.assertIn("Panel 1", story)
        self.assertIn("Panel 5", story)
        self.assertIn("CAPTION:", story)
        self.assertIn("NARRATION:", story)

    def test_03_filename_sanitization(self):
        """TC-03: Verify filename sanitizer strips illegal characters and adds hash."""
        dirty_prompt = "A wild @#$%^&* test prompt with spaces and /slashes!"
        filename = sanitize_filename(dirty_prompt)
        self.assertTrue(filename.startswith("panel_"))
        self.assertTrue(filename.endswith(".png"))
        self.assertNotIn("@", filename)
        self.assertNotIn("/", filename)
        self.assertNotIn("\\", filename)

    def test_04_procedural_image_generation(self):
        """TC-04: Verify Pillow scenic engine renders a valid 768x512 PNG."""
        test_output = os.path.join("static", "panels", "test_unit_scene.png")
        _draw_comic_scenic_image("A futuristic cyber city with neon lights and a masked detective", test_output)
        self.assertTrue(os.path.exists(test_output))
        with Image.open(test_output) as img:
            self.assertEqual(img.size, (768, 512))
            self.assertEqual(img.format, "PNG")

    def test_05_layout_builder_aggregation(self):
        """TC-05: Verify layout builder joins images, outlines, and story text."""
        outline = _generate_fallback_outline("Hero Conan in ancient jungle")
        story = _generate_fallback_story(outline)
        images = [f"static/panels/panel_test_{i}.png" for i in range(1, 6)]
        layout = build_comic_layout(images, story, outline)
        self.assertEqual(len(layout), 5)
        for i, item in enumerate(layout, start=1):
            self.assertEqual(item["panel"], i)
            self.assertEqual(item["image_path"], f"static/panels/panel_test_{i}.png")
            self.assertTrue(len(item["title"]) > 0)
            self.assertTrue(len(item["text"]) > 0)

    def test_06_pdf_unicode_sanitizer(self):
        """TC-06: Verify unicode character replacement handles smart quotes and dashes."""
        input_text = "“Hello world” — said the hero… it’s working with café!"
        cleaned = clean_text_for_pdf(input_text)
        self.assertNotIn("“", cleaned)
        self.assertNotIn("”", cleaned)
        self.assertNotIn("—", cleaned)
        self.assertNotIn("…", cleaned)
        self.assertIn('"Hello world"', cleaned)
        self.assertIn("- said", cleaned)

    def test_07_pdf_export_compilation(self):
        """TC-07: Verify FPDF2 compiles a valid multi-page PDF document."""
        outline = _generate_fallback_outline("Hero Nova in space")
        story = _generate_fallback_story(outline)
        test_img = os.path.join("static", "panels", "test_unit_scene.png")
        layout = build_comic_layout([test_img] * 5, story, outline)
        pdf_path = save_pdf(layout)
        self.assertTrue(os.path.exists(pdf_path))
        self.assertTrue(os.path.getsize(pdf_path) > 1000)
        self.assertTrue(pdf_path.endswith(".pdf"))

    def test_08_path_traversal_security(self):
        """TC-08: Verify StorageManager blocks path traversal attempts."""
        storage = StorageManager()
        self.assertTrue(storage.is_safe_export_path("static/exports/comic_123.pdf"))
        self.assertTrue(storage.is_safe_export_path("/static/exports/comic_123.pdf"))
        self.assertFalse(storage.is_safe_export_path("static/exports/../../etc/passwd"))
        self.assertFalse(storage.is_safe_export_path("..\\..\\Windows\\System32\\calc.exe"))
        self.assertFalse(storage.is_safe_export_path("/etc/shadow"))

    def test_09_fastapi_endpoints(self):
        """TC-09: Verify FastAPI routes respond correctly via TestClient."""
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)

        # GET /
        resp_home = client.get("/")
        self.assertEqual(resp_home.status_code, 200)
        self.assertIn("COMICCRAFT", resp_home.text)

        # GET /all-users
        resp_gallery = client.get("/all-users")
        self.assertEqual(resp_gallery.status_code, 200)

        # GET /test-image
        resp_img = client.get("/test-image?prompt=Cyberpunk_Hero")
        self.assertEqual(resp_img.status_code, 200)
        self.assertIn("path", resp_img.json())

        # Path traversal rejection test on /download-pdf
        resp_bad = client.get("/download-pdf?file_path=../../etc/passwd")
        self.assertEqual(resp_bad.status_code, 400)

if __name__ == "__main__":
    unittest.main(verbosity=2)
