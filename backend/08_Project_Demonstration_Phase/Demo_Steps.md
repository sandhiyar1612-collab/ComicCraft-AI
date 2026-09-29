# 📋 Live Demonstration Step-by-Step Script

This checklist provides a clear, repeatable guide for conducting an evaluative demonstration of ComicCraft.

---

## Pre-Flight Setup
1. Open PowerShell or Terminal in the repository root (`d:/comic`).
2. Run the application launcher:
   ```bash
   python run.py
   ```
3. Ensure the server starts on `http://127.0.0.1:8000`.

---

## Step-by-Step Demonstration Steps

| Step | Action | Expected Visual / Behavioral Outcome |
| :---: | :--- | :--- |
| **1** | Open browser to [http://127.0.0.1:8000](http://127.0.0.1:8000) | Homepage loads with vintage halftone comic paper texture, Ben-Day dots, and bold black ink borders. |
| **2** | Inspect the Google Gemini API Key bar | Key connection status badge is visible (`CONNECTED` if key present). |
| **3** | Click the preset badge: **Enchanted Forest** | Form fields instantly populate with: Prompt about an enchanted forest, Character *"Rusty the Fox"*, Setting *"Ancient Whispering Woods"*, Tone *"Wonder and Mystery"*. |
| **4** | Click **💥 CREATE COMIC BOOK 💥** | Comic flipbook modal appears with a rotating comic starburst, progress bar, and animated inking status messages. |
| **5** | Wait for redirection (~3 to 10 seconds) | Page redirects to `comic_preview.html` displaying 5 sequential comic panels. |
| **6** | Scroll through the 5 panels | Each panel displays the rendered scene artwork, action badge (*POW!*, *BAM!*), scene description box, and formatted character dialogue. |
| **7** | Click **📥 DOWNLOAD PRINTABLE PDF** | Browser triggers download of `comic_{timestamp}.pdf`. |
| **8** | Open the downloaded PDF file | PDF opens showing clean A4 pagination, double ink borders, yellow header bars, and custom TrueType comic fonts. |
| **9** | Click **Comic Vault** or visit [http://127.0.0.1:8000/all-users](http://127.0.0.1:8000/all-users) | Gallery displays all generated comic issues with timestamps and file sizes in KB. |
| **10**| Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Interactive Swagger UI opens with all REST endpoints (`/generate`, `/generate-comic/json`, `/all-users`, `/download-pdf`). |
| **11**| In terminal, run: `python 06_Project_Testing_Phase/test_suite.py` | Automated test suite executes and prints `Ran 9 tests ... OK` with 100% pass rate. |
