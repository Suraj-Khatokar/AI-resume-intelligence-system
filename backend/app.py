from flask import Flask, jsonify, request
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

        cur.execute("SELECT * FROM test_users")
        users = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"users": users})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
