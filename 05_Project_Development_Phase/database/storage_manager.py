"""
Filesystem Storage Manager for ComicCraft
Handles indexing, path security validation, and metadata extraction for generated comics and panel images.
"""
import os
import glob
from datetime import datetime
from typing import List, Dict, Optional

class StorageManager:
    """
    Manages persistent filesystem storage for comic book assets.
    """
    def __init__(self, exports_dir: str = "static/exports", panels_dir: str = "static/panels"):
        self.exports_dir = exports_dir
        self.panels_dir = panels_dir
        os.makedirs(self.exports_dir, exist_ok=True)
        os.makedirs(self.panels_dir, exist_ok=True)

    def list_exported_comics(self) -> List[Dict]:
        """
        Retrieves all generated comic PDFs sorted reverse-chronologically.
        """
        pattern = os.path.join(self.exports_dir, "*.pdf")
        export_files = glob.glob(pattern)
        comics = []
        for file_path in sorted(export_files, key=os.path.getmtime, reverse=True):
            try:
                stat = os.stat(file_path)
                created_dt = datetime.fromtimestamp(stat.st_mtime).strftime("%b %d, %Y %I:%M %p")
                web_path = "/" + file_path.replace("\\", "/")
                comics.append({
                    "filename": os.path.basename(file_path),
                    "file_path": file_path,
                    "web_path": web_path,
                    "created_at": created_dt,
                    "size_kb": round(stat.st_size / 1024, 1)
                })
            except OSError:
                continue
        return comics

    def is_safe_export_path(self, target_path: str) -> bool:
        """
        Validates that a path is strictly contained within the exports directory
        to prevent directory traversal attacks.
        """
        clean_path = os.path.normpath(target_path.lstrip("/\\"))
        normalized_export = os.path.normpath(self.exports_dir)
        return clean_path.startswith(normalized_export)

    def get_comic_path(self, filename: str) -> Optional[str]:
        """
        Returns absolute path to a comic if it exists in the exports directory.
        """
        safe_name = os.path.basename(filename)
        candidate = os.path.join(self.exports_dir, safe_name)
        if os.path.exists(candidate) and os.path.isfile(candidate):
            return candidate
        return None
