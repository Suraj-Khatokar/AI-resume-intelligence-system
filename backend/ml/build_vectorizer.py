import psycopg2
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="ai_resume_dg",
        user="postgres",
        password="user"
    )

def fetch_all_resume_texts():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT resume_text FROM resumes WHERE resume_text IS NOT NULL")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # Extract text from tuples
    texts = [row[0] for row in rows if row[0]]
    return texts

def build_and_save_vectorizer():
    texts = fetch_all_resume_texts()

    if not texts:
        print("No resume text found in database.")
        return

    vectorizer = TfidfVectorizer(stop_words="english")
    vectorizer.fit(texts)

    joblib.dump(vectorizer, "vectorizer.pkl")
    print("Vectorizer trained and saved successfully!")
    print("Vocabulary size:", len(vectorizer.vocabulary_))
if __name__ == "__main__":
    build_and_save_vectorizer()