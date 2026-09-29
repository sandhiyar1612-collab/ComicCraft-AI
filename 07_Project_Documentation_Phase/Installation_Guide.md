# ⚙️ Installation & Setup Guide

This guide provides step-by-step instructions for installing and running **ComicCraft** on Windows, macOS, and Linux.

---

## 1. Prerequisites
- **Python**: Version **3.10, 3.11, or 3.12** installed on your system.
  - Windows: Download from [python.org](https://www.python.org/downloads/) (ensure *"Add Python to PATH"* is checked during installation).
  - macOS: Install via Homebrew: `brew install python@3.12`
  - Linux (Ubuntu/Debian): `sudo apt update && sudo apt install python3 python3-pip python3-venv`
- **Git** (optional, for version control).

---

## 2. Setting Up the Workspace

Navigate to the project root directory:
```bash
cd d:/comic
```

### Create a Python Virtual Environment

**On Windows (PowerShell / Command Prompt)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
# If PowerShell script execution is restricted, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

**On macOS / Linux (Bash / Zsh)**:
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Dependencies Installed:
- `fastapi` & `uvicorn` (Web application and ASGI server)
- `jinja2` & `python-multipart` (HTML templates and form handling)
- `google-generativeai` (Google Gemini SDK)
- `fpdf2` & `pillow` (PDF rendering and image processing)
- `requests` & `python-dotenv` & `pydantic` (HTTP client and configuration)

---

## 4. Environment Variables Configuration
Copy the sample environment file `.env.example` to `.env`:

**Windows (PowerShell)**:
```powershell
Copy-Item .env.example .env
```

**macOS / Linux**:
```bash
cp .env.example .env
```

Open `.env` and add your Google Gemini API key:
```env
# Google Gemini API Key from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Application Host & Port
HOST=127.0.0.1
PORT=8000
```
*(Note: An API key is optional. ComicCraft includes offline fallback engines that generate complete comics without cloud keys).*

---

## 5. Starting the Server

You can launch ComicCraft using either of the following commands from the project root:

### Option A: Using the Root Launcher (Recommended)
```bash
python run.py
```

### Option B: Using Uvicorn Directly
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 6. Verifying the Installation
1. Open your browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)
2. Verify interactive API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3. Run the automated test suite to confirm all components are operational:
```bash
python 06_Project_Testing_Phase/test_suite.py
```
Expected result: `Ran 9 tests ... OK`.
