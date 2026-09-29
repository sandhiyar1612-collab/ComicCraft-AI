"""
Convenience Runner Script for ComicCraft
Starts the Uvicorn development server with hot-reloading.
"""
import sys
import uvicorn
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    print("=" * 60)
    print("[*] STARTING COMICCRAFT DEVELOPMENT SERVER")
    print("=" * 60)
    print("Serving from:", root_dir)
    print("Web Application URL: http://127.0.0.1:8000")
    print("Swagger UI Docs:     http://127.0.0.1:8000/docs")
    print("Comic Vault Gallery: http://127.0.0.1:8000/all-users")
    print("=" * 60)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
