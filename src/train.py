import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import mlflow
import mlflow.sklearn

from src.preprocess import clean_text

# Set local MLflow experiment name
EXPERIMENT_NAME = "SMS_Spam_Classifier"
mlflow.set_experiment(EXPERIMENT_NAME)


def load_data(filepath: str) -> pd.DataFrame:
    """Loads SMS spam dataset assuming tab-separated format (label, text)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    
    df = pd.read_csv(
        filepath, 
        sep="\t", 
        header=None, 
        names=["label", "text"]
    )
    df["target"] = df["label"].map({"spam": 1, "ham": 0})
    return df


def train_and_evaluate(model_type: str = "naive_bayes"):
    """
    Trains an NLP Pipeline and logs metrics/artifacts to MLflow.
    """
    print(f"\n🚀 Starting MLflow Run for model: {model_type}")

    # 1. Load Data
    data_path = "data/sms_spam.csv"
    df = load_data(data_path)

    # 2. Split Train / Test (80 / 20)
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], 
        df["target"], 
        test_size=0.2, 
        random_state=42, 
        stratify=df["target"]
    )

    # 3. Define Model
    if model_type == "naive_bayes":
        classifier = MultinomialNB(alpha=1.0)
        params = {"alpha": 1.0}
    elif model_type == "logistic_regression":
        classifier = LogisticRegression(C=1.0, max_iter=1000)
        params = {"C": 1.0, "max_iter": 1000}
    else:
        raise ValueError(f"Unsupported model_type: {model_type}")

    # 4. Build Pipeline with custom preprocessor
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(preprocessor=clean_text, max_features=5000)),
        ("clf", classifier)
    ])

    # 5. MLflow Tracking Context
    with mlflow.start_run(run_name=f"{model_type}_run"):
        # Log Parameters
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("data_path", data_path)
        mlflow.log_param("tfidf_max_features", 5000)
        for key, val in params.items():
            mlflow.log_param(f"clf_{key}", val)

        # Train Pipeline
        pipeline.fit(X_train, y_train)

        # Predict
        y_pred = pipeline.predict(X_test)

        # Compute Metrics
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)

        # Log Metrics
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("accuracy", accuracy)

        # Save Pipeline Model to MLflow using cloudpickle
        mlflow.sklearn.log_model(
            pipeline, 
            artifact_path="model",
            serialization_format="cloudpickle"
        )

        print(f"✅ Run Completed!")
        print(f"📊 Precision: {precision:.4f} | Recall: {recall:.4f} | F1: {f1:.4f} | Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    train_and_evaluate("naive_bayes")
    train_and_evaluate("logistic_regression")