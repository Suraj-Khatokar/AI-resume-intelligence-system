from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="ai_resume_dg",
        user="postgres",
        password="user"
    )
    return conn

@app.route("/")
def home():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"message": "Backend connected to PostgreSQL successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
