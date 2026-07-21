Here is a concise yet highly structured summary of what is expected for
  the Spam SMS Classifier project:

  ### 🎯 The Core Objective

  You are building an end-to-end spam detection API that uses text
  classification (NLP) and is wrapped in a production monitoring and
  versioning framework (MLOps).
  ──────
  ### 🛠️ The 5 Components You Will Build

  1. preprocess.py: A module to clean raw SMS texts (lowercase, remove
  punctuation, strip stop-words, and apply stemming/lemmatization).
  2. train.py: A training pipeline using a scikit-learn Pipeline
  (TfidfVectorizer + MultinomialNB or LogisticRegression).
  3. app.py: A FastAPI application exposing a /predict endpoint that
  takes raw text, validates it using Pydantic, and returns the
  classification (spam/ham) with its probability.
  4. database.py: An SQLite logger via SQLAlchemy that automatically
  saves every API request, timestamp, and response for auditing.
  5. monitor.py: A drift detection script that compares incoming SQLite
  logs with your training dataset to output a visual HTML report.
  ──────
  ### ⚙️ How the MLOps Stack Fits In

  • DVC (Data Version Control): Tracks the raw dataset file (sms_spam.
  csv) locally so it's not stored directly in Git.
  • MLflow: Logs hyperparameters (vocabulary size, vectorizer parameters,
  classifier alpha/C), metrics (specifically Precision, Recall, and F1-
  score due to the imbalanced nature of spam datasets), and saves the
  trained model binary.
  • SQLite: Acts as your production transaction log for request-response
  data auditing.
  • Evidently: Analyzes those SQLite production logs against the training
  baseline to detect if the text distribution shifts (e.g., if users
  start sending longer messages or new slang).
  • Docker: Containers are used to package the API and database logs for
  environment consistency.

────────────────────────────────────────────────────────────
> more specifications and what are the reuirements as per the currculum

● Read(C:/Users/HP/onedrive/d...ACHING-INSTRUCTIONS.md) (ctrl+o to expand)

  Based on the curriculum’s master index (INDEX.md) and the teaching
  instructions (AI-TEACHING-INSTRUCTIONS.md), here are the exact
  requirements and specifications defined by your curriculum:
  ──────
  ### 1. Curriculum Requirements (The "Must-Haves")

  • Dataset Versioning: Must initialize DVC, configure a local remote
  folder to act as storage, version control the spam dataset, and add the
  dataset's .dvc tracking file to Git.
  • Experiment Tracking: Must log parameters, metrics, and models to
  MLflow, and compare at least two distinct training runs (such as Naive
  Bayes vs. Logistic Regression).
  • Text Preprocessing: Must implement tokenisation, stop-word removal,
  and stemming/lemmatisation.
  • Imbalanced Data Metrics: Must track and optimize Precision, Recall,
  and F1-score, rather than raw accuracy.
  • API Serving: Serve predictions using FastAPI and store both request
  payloads and prediction responses directly to SQLite.
  • Drift Detection: Integrate Evidently to analyze incoming API text
  distribution vs. the baseline training distribution.
  • Retraining Pipeline: Simulate retraining triggered by detected drift
  via a GitHub Actions workflow.
  • Documentation: Provide a README that includes screenshots of your
  MLflow experiment dashboards and at least two Architecture Decision
  Records (ADRs) comparing tech choices.
  ──────
  ### 2. Core Concepts You Must Master (As per the Study Prompts)

  • TF-IDF Intuition: Understand why TF-IDF weighting is superior to raw
  word counts for classification.
  • Precision vs. Recall Trade-Off: Understand the implications in spam
  classification (e.g., classifying a critical email/SMS as spam—low
  precision—vs. letting spam slide through to the inbox—low recall).
  • DVC Git Analogy: Master the workflow of tracking data hashes in Git
  while pushing the actual heavy content to DVC storage.
  • Data Drift vs. Concept Drift: Be able to diagnose performance drop-
  offs (e.g., when users send messages with new slang or shorthand).
  ──────
  ### 3. The 7 Files/Deliverables Expected in the Folder

  1. data/sms_spam.csv.dvc: The Git-tracked DVC hash pointer representing
  your dataset.
  2. notebooks/01_eda_and_baseline.ipynb: Initial exploration notebook.
  3. src/preprocess.py: Clean, tokenized, and normalized text processor.
  4. src/train.py: Python script containing the MLflow runs.
  5. src/app.py: FastAPI app with database connection integrations.
  6. src/monitor.py: The script triggering Evidently's HTML report output.
  7. tests/: A testing suite validating your text cleaning functions and
  API endpoints.







