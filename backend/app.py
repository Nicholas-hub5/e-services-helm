from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def connect_db():
    return psycopg2.connect(
        host="t2s-postgres",
        database="t2sdb",
        user="t2suser",
        password="t2spassword"
    )

@app.route("/api/enroll", methods=["POST"])
def enroll():
    data = request.get_json()
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO enrollments (first_name, last_name, phone, email, course) VALUES (%s, %s, %s, %s, %s)",
            (data["firstName"], data["lastName"], data["phone"], data["email"], data["course"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return "Enrollment successful!", 200
    except Exception as e:
        return str(e), 500
