───────────────────────────────────────────────────────┐
│ 1. Pydantic Request Validation (SMSRequest)             │
│    Rejects invalid JSON payloads automatically         │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Lifespan ML Model (Option B)                         │
│    Reads loaded MLflow pipeline directly from RAM      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Database Audit Logging (src/database.py)             │
│    Writes (raw_text, prediction, proba) to SQLite      │
└────────────────────────────────────────────────────────┘