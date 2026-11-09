# SYLTHEN

## Ethical Spyware Simulation & Detection Framework

SYLTHEN is a controlled cybersecurity research framework designed to simulate spyware-like telemetry in an authorized laboratory environment and demonstrate how suspicious behavioral patterns can be detected.

The project focuses on the defensive side of spyware research: secure telemetry collection, authenticated encryption, encrypted evidence storage, rule-based detection, behavioral analysis, risk scoring, and security reporting.

> **Safety Notice:** SYLTHEN is designed exclusively for authorized laboratory experimentation. It does not perform covert system-wide keylogging, credential capture, persistence, evasion, or unauthorized data collection.

---

## Architecture

```text
Authorized Lab Simulator
        │
        ▼
Telemetry Collector
        │
        ▼
AES-256-GCM Encryption
        │
        ▼
Encrypted SQLite Storage
        │
        ▼
Authorized Decryption
        │
        ▼
Detection Engine
        │
        ├── Detection Rules
        ├── Risk Scoring
        └── Behavioral Analysis
        │
        ▼
FastAPI REST API
        │
        ▼
React + TypeScript Dashboard
```

## Windows quick start

From the repository root in Windows PowerShell, create a virtual environment and install the desktop demo and test dependencies. This setup was tested with Python 3.14 on Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-demo.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m backend.demo
```

For a quick check, hold one lowercase key for a second inside the lab text box, release it, and select **Run Security Analysis**. In a fresh session, expect one event and zero findings.
