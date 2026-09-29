# 📋 Master Test Plan

## 1. Test Objectives
The primary objective of testing ComicCraft is to verify:
1. **Pipeline Determinism**: Ensure that the 5-stage pipeline executes reliably from user input to completed PDF without runtime exceptions.
2. **Defensive Failover Integrity**: Validate that if external AI APIs (Gemini Flash, Gemini Pro, Imagen 3) are offline, rate-limited, or encounter invalid keys, internal algorithmic and procedural fallbacks execute seamlessly.
3. **Security Posture**: Confirm that path traversal vulnerabilities cannot be exploited via file download endpoints and that API keys are protected.
4. **Data & Typography Fidelity**: Verify that non-standard unicode characters, comic book fonts, and panel dimensions adhere to publishing standards.

---

## 2. Test Scope & Levels

```
┌──────────────────────────────────────────────────────────────┐
│                        TESTING LEVELS                        │
├────────────────────┬─────────────────────────────────────────┤
│ Unit Testing       │ Fallback outline, story script parsing, │
│                    │ filename sanitization, unicode filters  │
├────────────────────┼─────────────────────────────────────────┤
│ Integration Testing│ Pillow Ben-Day procedural drawing,      │
│                    │ layout builder aggregation, FPDF2 export│
├────────────────────┼─────────────────────────────────────────┤
│ API / Contract     │ FastAPI endpoints (GET /, /all-users,   │
│ Testing            │ /test-image, POST /generate-comic/json) │
├────────────────────┼─────────────────────────────────────────┤
│ Security Testing   │ Path traversal boundary tests on        │
│                    │ /download-pdf endpoint                  │
└────────────────────┴─────────────────────────────────────────┘
```

---

## 3. Test Environment Specifications
- **Operating System**: Microsoft Windows 11 / 10.
- **Python Runtime**: Python 3.12.10.
- **Testing Libraries**:
  - `unittest` (Standard Library test runner)
  - `fastapi.testclient.TestClient` (HTTP integration harness)
  - `Pillow` (Image verification)
  - `fpdf2` (PDF verification)

---

## 4. Defect Severity Classification

| Severity Level | Definition | Example |
| :--- | :--- | :--- |
| **Critical (P1)** | Complete system crash, unhandled 500 error on valid input | PDF compilation failure or unhandled exception on API timeout |
| **Major (P2)** | Core feature unusable, no workaround | Images fail to render or outline missing required JSON keys |
| **Medium (P3)** | Secondary feature degraded or formatting glitch | Missing custom font causing text overflow or spacing error |
| **Minor (P4)** | Cosmetic or documentation typo | Label misalignment or console notice |

---

## 5. Pass / Fail Criteria
- **Pass Criteria**: 100% of unit, integration, and security test cases must pass without unhandled exceptions.
- **Fail Criteria**: Any test case failing assertion, throwing uncaught exceptions, or permitting directory traversal.
