from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from services.file_parser import extract_resume_text

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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


# Home route - checks DB connection
@app.route("/")
def home():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"message": "Backend connected to PostgreSQL successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST route to add user (React-ready)
@app.route("/add-user", methods=["POST"])
def add_user():
    try:
        data = request.get_json()

        if not data or "name" not in data:
            return jsonify({"error": "Name is required"}), 400

        name = data["name"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO test_users (name) VALUES (%s)", (name,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"User {name} added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET route to fetch all users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM test_users")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "name": row[1]
            })

        return jsonify({"users": users})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/update-user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()

        if not data or "name" not in data:
            return jsonify({"error": "Name is required"}), 400

        name = data["name"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE test_users SET name = %s WHERE id = %s",
            (name, user_id)
        )
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"User {user_id} updated successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/delete-user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM test_users WHERE id = %s", (user_id,))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": f"User {user_id} deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/add-resume", methods=["POST"])
def add_resume():
    try:
        data = request.get_json()

        required_fields = ["name", "email", "skills", "resume_text"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Name, email, skills, and resume_text are required"}), 400

        name = data["name"]
        email = data["email"]
        skills = data["skills"]
        resume_text = data["resume_text"]

        # --- Keyword-Based Scoring ---
        REQUIRED_SKILLS = [
            "python",
            "sql",
            "machine learning",
            "react",
            "flask",
            "docker"
        ]

        skills_list = [s.strip().lower() for s in skills.split(",")]

        matched_skills = [
            skill for skill in REQUIRED_SKILLS
            if skill in skills_list
        ]

        score = (len(matched_skills) / len(REQUIRED_SKILLS)) * 100

        # --- Store in Database ---
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO resumes (name, email, skills, score, resume_text)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, skills, score, resume_text))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "message": "Resume added successfully",
            "matched_skills": matched_skills,
            "score": score
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/resumes", methods=["GET"])
def get_resumes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, email, skills, score, created_at FROM resumes")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        resumes = []
        for row in rows:
            resumes.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "skills": row[3],
                "score": row[4],
                "created_at": row[5]
            })

        return jsonify({"resumes": resumes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/resumes/top", methods=["GET"])
def get_top_resumes():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name, email, skills, score, created_at
            FROM resumes
            ORDER BY score DESC
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        resumes = []
        for row in rows:
            resumes.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "skills": row[3],
                "score": row[4],
                "created_at": row[5]
            })

        return jsonify({"top_resumes": resumes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/resumes/filter", methods=["GET"])
def filter_resumes():
    try:
        skill = request.args.get("skill")

        if not skill:
            return jsonify({"error": "Skill query parameter is required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # ILIKE makes it case-insensitive in PostgreSQL
        cur.execute("""
            SELECT id, name, email, skills, score, created_at
            FROM resumes
            WHERE skills ILIKE %s
            ORDER BY score DESC
        """, (f"%{skill}%",))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        resumes = []
        for row in rows:
            resumes.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "skills": row[3],
                "score": row[4],
                "created_at": row[5]
            })

        return jsonify({"filtered_resumes": resumes})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
