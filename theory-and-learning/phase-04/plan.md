

 🗺️ Phase 4 Master Execution Plan

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Synthetic Traffic & Drift Detection (src/monitor.py)│
│ Populate SQLite with sample requests -> Evidently HTML Report│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Automated API Unit Testing (tests/test_app.py)      │
│ Pytest coverage for /health and /predict using TestClient   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Application Containerization (Dockerfile)           │
│ Multi-stage / optimized build for FastAPI + SQLite + ML model│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: CI/CD Pipeline & Architecture Decision Records      │
│ GitHub Actions workflow + ADR documentation                 │
└─────────────────────────────────────────────────────────────┘

```

---

### Step 1: Synthetic Traffic & Drift Detection (`src/monitor.py`)

* **Problem to Solve:** Statistical drift testing requires a statistically significant sample size ($N \ge 30-50$ requests). Our SQLite database currently has only 1 manual entry.
* **Deliverable 1.1:** A lightweight simulation helper (`src/simulate_traffic.py`) that sends 50 diverse SMS payloads (normal messages + spam) to `[http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict)`.
* **Deliverable 1.2:** `src/monitor.py` built with **Evidently AI**. It loads `data/sms_spam.csv` as reference data and `production_audit.db` as current data, calculating text length, vocabulary, and prediction confidence drift.
* **Artifact:** `reports/drift_report.html` (interactive visual dashboard).

---

### Step 2: Automated API Unit Testing (`tests/test_app.py`)

* **Problem to Solve:** Ensure future code changes don't break our API response structure or return invalid HTTP status codes.
* **Deliverable:** `tests/test_app.py` using `starlette.testclient.TestClient`.
* **Coverage Targets:**
1. `GET /health` returns `200 OK` and `"model_loaded": true`.
2. `POST /predict` with valid spam text returns `200 OK` with keys `prediction`, `label`, and `probability`.
3. `POST /predict` with invalid body (e.g., empty string or non-string payload) triggers Pydantic's `422 Unprocessable Entity`.


* **Verification:** `.\venv\Scripts\python.exe -m pytest` running all 8+ unit tests.

---

### Step 3: Application Containerization (`Dockerfile`)

* **Problem to Solve:** Ensure the API runs identically on any environment (Linux cloud VMs, Kubernetes, Docker Desktop) without dependency mismatch.
* **Deliverable:** `Dockerfile` in project root.
* **Specifications:**
* Base image: `python:3.11-slim` or `python:3.13-slim`.
* Installs requirements from `pyproject.toml` / `requirements.txt`.
* Copies `src/`, `data/`, and `mlruns/` trained model binaries.
* Exposes port `8000` and launches Uvicorn server.


* **Verification:** `docker build -t spam-classifier:latest .` and local run test.

---

### Step 4: CI/CD Pipeline & Architecture Documentation (ADRs)

* **Problem to Solve:** Automate verification on every Git commit and document engineering tradeoffs for portfolio review.
* **Deliverable 4.1:** `.github/workflows/ci.yml`
* Triggers on `git push` or `pull_request` to `main`.
* Sets up Python environment, installs dependencies in editable mode (`pip install -e .`), and runs `pytest`.


* **Deliverable 4.2:** Architecture Decision Records in `docs/adr/`:
* `0001-model-selection-and-storage.md` (Naive Bayes vs. Logistic Regression & MLflow artifact storage).
* `0002-sqlite-audit-logging-strategy.md` (FastAPI lifespan model loading & transaction logging design).



---

### 🏁 Summary of Phase 4 Outputs

| Component | File Path | Success Criteria |
| --- | --- | --- |
| **Traffic Simulator** | `src/simulate_traffic.py` | Populates $\ge 50$ rows in `production_audit.db` |
| **Drift Monitor** | `src/monitor.py` | Generates browser-viewable `reports/drift_report.html` |
| **API Test Suite** | `tests/test_app.py` | All endpoint unit tests pass in `pytest` |
| **Container Spec** | `Dockerfile` | Image builds and serves `/predict` on port `8000` |
| **CI Automation** | `.github/workflows/ci.yml` | Automated pipeline passes on push |
| **Documentation** | `docs/adr/*.md` | Standard markdown records explaining system architecture |

---