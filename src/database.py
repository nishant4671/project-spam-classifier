from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Define SQLite Database URL
DATABASE_URL = "sqlite:///./production_audit.db"

# 2. Create SQLAlchemy Engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Required for SQLite in multi-threaded FastAPI
)

# 3. Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Declarative Base Model
Base = declarative_base()


class PredictionLog(Base):
    """
    SQLAlchemy Table Schema for logging API predictions.
    """
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(String, nullable=False)
    prediction = Column(Integer, nullable=False)      # 1 = Spam, 0 = Ham
    label = Column(String, nullable=False)           # "spam" or "ham"
    probability = Column(Float, nullable=False)      # Confidence score (0.0 to 1.0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    """Creates tables in SQLite database if they don't exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI Dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()