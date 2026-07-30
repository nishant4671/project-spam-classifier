Welcome to **Phase 2**! 

Now that you have a working `preprocess.py` and passing tests, it’s time to step out of "Jupyter notebook" territory and into **production-grade MLOps**. 

Here is the brutal truth about real-world ML:

- **Data changes**. The "spam" you trained on last week looks different today (new slang, new scams).
- **Experiments multiply**. You will train 50 different models with different parameters. If you don't track them, you'll forget *which* model performed the best and *which data* was used.

**DVC** fixes the data problem. **MLflow** fixes the experiment tracking problem. Here is exactly how to set them up in your project.

---

### 🗂️ Part A: DVC (Data Version Control) – "Git for Giant Datasets"

**The Problem:** You can't put a 500MB CSV file on GitHub. Git hates large files. 
**The Solution:** DVC stores the actual data in cloud storage (or a local drive) and stores only a tiny **pointer file** (`.dvc`) in your Git repository. 

#### Step 1: Installation & Initialization
Make sure your `venv` is activated. Install DVC and initialize it in your project root.

```bash
pip install dvc

# Initialize DVC in your current project folder (creates .dvc/ folder)
dvc init

# IMPORTANT: Commit the .dvc folder to Git so your teammates get the same setup
git add .dvc/
git commit -m "Initialize DVC"
```

#### Step 2: Configure Remote Storage (Where the actual data lives)
Think of this like a "cloud drive" for your data. For learning, we will use a **local remote** (a folder on your hard drive). In production, you'd use S3, GCS, or Azure.

```bash
# Create a folder on your machine to act as the "remote storage"
mkdir /tmp/dvc-storage

# Tell DVC to use this folder as the default remote
dvc remote add -d storage /tmp/dvc-storage
```

#### Step 3: Track Your Dataset (The Magic)
Assuming you have a raw dataset file at `data/raw/spam_data.csv`. Tell DVC to track it.

```bash
# This replaces 'git add'. It copies the file to the remote storage
# and creates a tiny pointer file: data/raw/spam_data.csv.dvc
dvc add data/raw/spam_data.csv

# Now, add the tiny pointer file to Git (NOT the massive CSV file!)
git add data/raw/spam_data.csv.dvc
git commit -m "Track spam dataset with DVC"

# Push the actual data to your configured remote storage
dvc push
```

**The Workflow:** If you change the dataset next week, run `dvc add data/raw/spam_data.csv` again, commit the changed `.dvc` file, and `dvc push`. Git tracks the *version history*; DVC tracks the *actual bytes*.

---

### 🧪 Part B: MLflow – "Your Lab Notebook on Steroids"

**The Problem:** Did you get 98% precision with `C=1.0` or `C=0.5`? Which seed did you use? Where is that model file saved? 
**The Solution:** MLflow automatically logs **parameters** (hyperparameters), **metrics** (precision/recall), and **artifacts** (the saved model pickle file) for every single run.

#### Step 1: Installation
```bash
pip install mlflow
```

#### Step 2: Creating the Training Script (The Integration)
Let's imagine you are creating `src/train.py`. Here is how you wrap it with MLflow:

```python
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score
import pandas as pd

# Load your DVC-tracked data
df = pd.read_csv("data/raw/spam_data.csv")

# Preprocess (using your clean_text function)
df["clean_text"] = df["message"].apply(clean_text)

# Split & Vectorize
X = df["clean_text"]
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# --- MLFLOW STARTS HERE ---
# Start an MLflow run. This creates a unique folder for this experiment.
with mlflow.start_run() as run:
    
    # 1. LOG PARAMETERS (What settings did I use?)
    model_params = {"C": 1.0, "solver": "lbfgs", "max_iter": 1000}
    mlflow.log_params(model_params)
    
    # 2. TRAIN THE MODEL
    model = LogisticRegression(C=1.0, solver="lbfgs", max_iter=1000)
    model.fit(X_train_vec, y_train)
    
    # 3. PREDICT & EVALUATE
    y_pred = model.predict(X_test_vec)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # 4. LOG METRICS (How well did it perform?)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # 5. LOG THE ACTUAL MODEL FILE (Save it to MLflow)
    mlflow.sklearn.log_model(model, "spam_classifier")
    
    # 6. (Bonus) Log the vectorizer too, so predictions work later
    mlflow.log_artifact("vectorizer.pkl") 
    
    print(f"Run ID: {run.info.run_id}")
    print(f"Precision: {precision}, Recall: {recall}")
```

#### Step 3: Running Different Experiments (Hyperparameter Tuning)
Now, instead of manually changing `C` in your code, you can loop through different values or use a command-line argument.

```bash
# Run 1 (C=1.0)
python src/train.py --C 1.0

# Run 2 (C=0.1)
python src/train.py --C 0.1

# Run 3 (C=10.0)
python src/train.py --C 10.0
```
MLflow automatically organizes these as three separate "Runs" in one "Experiment".

#### Step 4: Visualizing the Results (The Dashboard)
This is the "wow" moment. In your terminal, run:

```bash
mlflow ui
```

This starts a local web server. Open your browser and go to **`http://127.0.0.1:5000`**.

You will see a beautiful table comparing all your runs side-by-side:
| Run ID | C (Parameter) | Precision (Metric) | Recall (Metric) | Model Artifact |
| :--- | :--- | :--- | :--- | :--- |
| 123abc | 1.0 | 0.98 | 0.95 | ⬇️ Download |
| 456def | 0.1 | 0.92 | 0.97 | ⬇️ Download |
| 789ghi | 10.0 | 0.96 | 0.90 | ⬇️ Download |

You can instantly see that `C=1.0` gives the best balance, and you can download that exact model file with one click to deploy it!

---

### 🧠 How DVC + MLflow Work Together (The Perfect Marriage)

| | **DVC** | **MLflow** |
| :--- | :--- | :--- |
| **What it tracks** | The **ingredients** (the raw spam CSV files). | The **recipe & result** (the hyperparameters and the trained model brain). |
| **The Question it answers** | *"Which exact 5,000 emails did I train on last Tuesday?"* | *"What C-value gave me 98% precision, and where is that model saved?"* |
| **How they connect** | You `dvc pull` to get the dataset. You run the training script. MLflow logs the model. You decide which MLflow model to deploy. |

---

### 🚀 Your Next Steps (Hands-On Commands)

Copy and run these in your terminal (in your project root):

```bash
# 1. Install the tools
pip install dvc mlflow

# 2. Set up DVC
dvc init
mkdir -p data/raw
# (Place your spam CSV file into data/raw/)
dvc add data/raw/spam_data.csv
git add data/raw/spam_data.csv.dvc
git commit -m "Add dataset with DVC"

# 3. Run your first MLflow experiment
python src/train.py

# 4. Open the MLflow UI to see your results (this runs forever, open a new terminal for this)
mlflow ui
```

**Warning:** `mlflow ui` will run on port 5000. If your FastAPI later uses port 8000, there is no conflict. If port 5000 is blocked, run `mlflow ui --port 5001`. 

