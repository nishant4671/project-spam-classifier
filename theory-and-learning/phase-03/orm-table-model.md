2. The ORM Table Model (PredictionLog)
Python
class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(String, nullable=False)
    prediction = Column(Integer, nullable=False)
    label = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
ORM (Object-Relational Mapping): Instead of writing raw SQL commands like CREATE TABLE prediction_logs (id INT...), SQLAlchemy lets us define our database table as a standard Python class.

Every instance of PredictionLog represents one row in our database table.

timestamp: Notice lambda: datetime.now(timezone.utc). Using a lambda ensures that every time a new row is created, SQLAlchemy evaluates the exact current time instead of fixing the time when the server starts up.