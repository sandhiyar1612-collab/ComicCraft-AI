# 🖥️ System Requirements Specification

## 1. Operating System & Platform Compatibility
- **Operating Systems**:
  - Microsoft Windows 10 / 11 (tested and active in environment).
  - Ubuntu Linux 20.04 / 22.04 LTS / Debian 11+.
  - macOS 12 Monterey or newer (Apple Silicon M1/M2/M3 and Intel).
- **Containerization**: Compatible with Docker Engine 20.10+ and Docker Compose v2+.

---

## 2. Software & Runtime Dependencies

### Core Runtime
- **Python**: Version **3.10, 3.11, or 3.12** (Active environment: Python 3.12.10).
- **Package Manager**: `pip` (v23.0+).

### Python Package Dependencies (`requirements.txt`)

| Package | Version Requirement | Primary Purpose |
| :--- | :--- | :--- |
| **`fastapi`** | `>= 0.110.0` | High-performance asynchronous web framework & API routing |
| **`uvicorn`** | `>= 0.28.0` | Production ASGI web server implementation |
| **`jinja2`** | `>= 3.1.3` | Server-side HTML template rendering engine |
| **`python-multipart`** | `>= 0.0.9` | Multipart/form-data parser for web form submissions |
| **`google-generativeai`**| `>= 0.4.0` | Official Google SDK for Gemini Flash & Pro LLMs |
| **`fpdf2`** | `>= 2.7.8` | High-precision PDF rendering and multi-page compilation |
| **`pillow`** | `>= 10.2.0` | Image processing, Ben-Day dots, gradients, and graphic drawing |
| **`requests`** | `>= 2.31.0` | Synchronous HTTP client for REST model calls |
| **`python-dotenv`** | `>= 1.0.1` | Environment variable management from `.env` |
| **`pydantic`** | `>= 2.6.0` | Strict data validation and settings management |

---

## 3. External API Prerequisites
- **Google Gemini API Key**:
  - Provider: Google AI Studio ([https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)).
  - Supported Models: `gemini-1.5-flash`, `gemini-2.0-flash`, `gemini-1.5-pro`, `imagen-3.0-generate-002`.
  - *Note*: An API key is optional for core operation due to ComicCraft's built-in intelligent offline procedural fallback engines.

---

## 4. Hardware Specifications

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **CPU** | 2-Core x86_64 or ARM64 processor | 4-Core modern processor (Intel i5/i7, AMD Ryzen, Apple Silicon) |
| **RAM** | 1 GB Free Memory | 4 GB+ RAM |
| **Disk Space** | 500 MB for source & dependencies | 2 GB+ (for accumulated comic PDF and image archives) |
| **GPU** | None required (zero GPU dependencies) | None required |
| **Network** | 1 Mbps internet connection (for cloud APIs) | 10 Mbps+ broadband connection |
