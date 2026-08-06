# Before we write the code, here are the 3 key layers working together inside src/app.py:

# ┌────────────────────────────────────────────────────────┐
# │ 1. Pydantic Request Validation (SMSRequest)             │
# │    Rejects invalid JSON payloads automatically         │
# └───────────────────────────┬────────────────────────────┘
#                             │
#                             ▼
# ┌────────────────────────────────────────────────────────┐
# │ 2. Lifespan ML Model (Option B)                         │
# │    Reads loaded MLflow pipeline directly from RAM      │
# └───────────────────────────┬────────────────────────────┘
#                             │
#                             ▼
# ┌────────────────────────────────────────────────────────┐
# │ 3. Database Audit Logging (src/database.py)             │
# │    Writes (raw_text, prediction, proba) to SQLite      │
# └────────────────────────────────────────────────────────┘










from contextlib import asynccontextmanager
from typing import Dict, Any
import os
import glob

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import mlflow.sklearn

from src.database import init_db, get_db, PredictionLog


# ------------------------------------------------------------------
# 1. Pydantic Schemas (Input/Output Contracts)
# ------------------------------------------------------------------
class SMSRequest(BaseModel):
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=1000, 
        example="WINNER!! You have won $1000 cash. Call now!"
    )


class SMSResponse(BaseModel):
    text: str
    prediction: int          # 1 = Spam, 0 = Ham
    label: str               # "spam" or "ham"
    probability: float       # Confidence score (0.0 to 1.0)


# Global variable to hold our loaded in-memory pipeline
ml_pipeline = None


# ------------------------------------------------------------------
# 2. FastAPI Lifespan Manager (Option B: Load Model on Startup)
# ------------------------------------------------------------------
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    global ml_pipeline
    print("\n⚡ Starting up FastAPI Server...")
    
    # Initialize SQLite Database Tables
    init_db()
    print("✅ Database initialized.")

    # Find trained MLflow model artifacts using pathlib (Windows-safe)
    mlruns_dir = Path("mlruns")
    model_dirs = list(mlruns_dir.rglob("artifacts/model"))
    
    if not model_dirs:
        # Fallback search for any MLmodel file if subfolder structure differs
        mlmodel_files = list(mlruns_dir.rglob("MLmodel"))
        if mlmodel_files:
            model_dirs = [f.parent for f in mlmodel_files]

    if not model_dirs:
        raise RuntimeError(
            "No MLflow trained model found! "
            "Ensure 'mlruns' directory exists and contains trained artifacts, "
            "or run 'python src/train.py' first."
        )
    
    # Pick the most recently modified trained model
    latest_model_path = str(max(model_dirs, key=lambda p: p.stat().st_mtime))
    print(f"📦 Loading trained pipeline from: {latest_model_path}")
    
    # Load pipeline ONCE into global memory
    ml_pipeline = mlflow.sklearn.load_model(latest_model_path)
    print("🚀 ML Pipeline loaded into memory successfully!\n")
    
    yield  # Server handles incoming API requests here
    
    print("🛑 Shutting down FastAPI Server...")

# ------------------------------------------------------------------
# 3. FastAPI App & Routes
# ------------------------------------------------------------------
app = FastAPI(
    title="Production Spam SMS Classifier API",
    description="Real-time SMS Spam detection with SQLite transaction logging.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    """Simple status check endpoint."""
    return {"status": "healthy", "model_loaded": ml_pipeline is not None}


@app.post("/predict", response_model=SMSResponse, status_code=status.HTTP_200_OK)
def predict_sms(payload: SMSRequest, db: Session = Depends(get_db)):
    """
    Predicts whether an incoming SMS is Spam or Ham, 
    and logs the request/response to the SQLite database.
    """
    if ml_pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Model is not initialized."
        )

    raw_text = payload.text

    # 1. Inference using pre-loaded pipeline
    # Pipeline handles: clean_text -> TF-IDF -> Classifier prediction
    prediction_array = ml_pipeline.predict([raw_text])
    probabilities = ml_pipeline.predict_proba([raw_text])

    pred_class = int(prediction_array[0])
    # Probability of class 1 (Spam)
    spam_probability = float(probabilities[0][1])
    label_str = "spam" if pred_class == 1 else "ham"

    # 2. Log transaction to SQLite database for production auditing
    log_entry = PredictionLog(
        raw_text=raw_text,
        prediction=pred_class,
        label=label_str,
        probability=spam_probability
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    # 3. Return response payload matching SMSResponse schema
    return SMSResponse(
        text=raw_text,
        prediction=pred_class,
        label=label_str,
        probability=round(spam_probability, 4)
    )