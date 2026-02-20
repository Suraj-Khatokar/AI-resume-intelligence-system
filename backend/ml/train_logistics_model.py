import psycopg2
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# -----------------------------
# CONFIG
# -----------------------------
THRESHOLD = 0.25

JOB_DESCRIPTION = """
We are hiring a Data Scientist with strong experience in Python,
Pandas, NumPy, Scikit-learn, Machine Learning, Deep Learning,
Statistics, Data Visualization, and SQL.
The candidate should be comfortable building predictive models,
performing feature engineering, and working with large datasets.
Experience with experimentation, model evaluation, and deployment is preferred.
"""

# -----------------------------
# 1️⃣ Fetch Data
# -----------------------------
conn = psycopg2.connect(
    dbname="ai_resume_dg",
    user="postgres",
    password="user",
    host="localhost",
    port="5432"
)

query = "SELECT id, resume_text FROM resumes;"
df = pd.read_sql(query, conn)

print("Total resumes:", len(df))

# -----------------------------
# 2️⃣ TF-IDF
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["resume_text"])

job_vector = vectorizer.transform([JOB_DESCRIPTION])

# -----------------------------
# 3️⃣ Generate Labels
# -----------------------------
similarities = cosine_similarity(X, job_vector).ravel()
y = (similarities >= THRESHOLD).astype(int)

print("Class Distribution:")
print(pd.Series(y).value_counts())

# -----------------------------
# 4️⃣ Train/Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 5️⃣ Train Logistic Regression
# -----------------------------
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train, y_train)

# -----------------------------
# 6️⃣ Evaluation
# -----------------------------
y_pred = model.predict(X_test)

print("\nEvaluation Metrics:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

import pickle

# Save trained model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save vectorizer
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully.")