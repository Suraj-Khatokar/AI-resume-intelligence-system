import psycopg2
import joblib
from sklearn.metrics.pairwise import cosine_similarity

# DB connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="ai_resume_dg",
        user="postgres",
        password="user"
    )

# Load vectorizer once
vectorizer = joblib.load("vectorizer.pkl")

def compute_similarity_with_all_resumes(job_description):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, resume_text FROM resumes WHERE resume_text IS NOT NULL")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    # Transform job description
    job_vector = vectorizer.transform([job_description])

    for row in rows:
        resume_id = row[0]
        name = row[1]
        resume_text = row[2]

        resume_vector = vectorizer.transform([resume_text])

        similarity = cosine_similarity(job_vector, resume_vector)[0][0]

        results.append({
            "id": resume_id,
            "name": name,
            "similarity_score": round(float(similarity), 4)
        })

    # Sort by similarity descending
    results.sort(key=lambda x: x["similarity_score"], reverse=True)

    return results