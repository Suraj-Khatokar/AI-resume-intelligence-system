import psycopg2
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# CONFIG
# -----------------------------
THRESHOLD = 0.25

JOB_DESCRIPTION = """
Looking for a Python backend developer with experience in Flask, REST APIs,
PostgreSQL, Docker, and cloud deployment.
"""

# -----------------------------
# 1️⃣ Connect to DBi 
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

# -----------------------------
# 2️⃣ TF-IDF Vectorization
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["resume_text"])

job_vector = vectorizer.transform([JOB_DESCRIPTION])

# -----------------------------
# 3️⃣ Compute Similarity
# -----------------------------
similarities = cosine_similarity(X, job_vector).ravel()

# -----------------------------
# 4️⃣ Generate Labels
# -----------------------------
df["similarity"] = similarities
df["label"] = (df["similarity"] >= THRESHOLD).astype(int)

# -----------------------------
# 5️⃣ Print Results
# -----------------------------
print("\nResume ID | Similarity | Label")
print("----------------------------------")

for _, row in df.iterrows():
    print(f"{row['id']} \t\t {row['similarity']:.3f} \t\t {row['label']}")

print("\nClass Distribution:")
print(df["label"].value_counts())