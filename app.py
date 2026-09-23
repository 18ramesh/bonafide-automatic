from flask import Flask, render_template, request, send_file
import sqlite3
import os
import pandas as pd

from pdf_generator import generate_bonafide


app = Flask(__name__)

DB_NAME = "college.db"
EXCEL_FILE = "students.xlsx"


# --------------------------------------------------
# Initialize database
# --------------------------------------------------

def initialize_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            course TEXT,
            department TEXT,
            semester TEXT,
            academic_year TEXT
        )
    """)

    conn.commit()

    # Check whether students already exist
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    # Import Excel data only if database is empty
    if count == 0 and os.path.exists(EXCEL_FILE):

        df = pd.read_excel(EXCEL_FILE)

        for _, row in df.iterrows():

            try:

                cursor.execute("""
                    INSERT OR IGNORE INTO students
                    (usn, name, course, department, semester, academic_year)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    str(row["USN"]).strip().upper(),
                    str(row["Name"]),
                    str(row["Course"]),
                    str(row["Department"]),
                    str(row["Semester"]),
                    str(row["Academic Year"])
                ))

            except Exception as e:

                print("Error importing student:", e)

        conn.commit()

        print("Excel student data imported successfully.")

    else:

        print(f"Database already contains {count} students.")

    conn.close()


# Initialize database when application starts
initialize_database()


# --------------------------------------------------
# Find student using exact USN
# --------------------------------------------------

def find_student_by_usn(usn):

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT usn, name, course, department, semester, academic_year
        FROM students
        WHERE usn = ?
    """, (usn.strip().upper(),))

    student = cursor.fetchone()

    conn.close()

    return student


# --------------------------------------------------
# Home page - Search student
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    student = None
    error = None

    if request.method == "POST":

        usn = request.form.get("usn", "").strip()

        if not usn:

            error = "Please enter a USN."

        else:

            student = find_student_by_usn(usn)

            if student is None:

                error = "Student not found. Please check the USN."

    return render_template(
        "index.html",
        student=student,
        error=error
    )


# --------------------------------------------------
# Generate Bonafide Certificate
# --------------------------------------------------

@app.route("/generate/<usn>")
def generate_certificate(usn):

    student = find_student_by_usn(usn)

    if student is None:

        return "Student not found", 404

    try:

        pdf_file = generate_bonafide(student)

        return send_file(
            pdf_file,
            as_attachment=True,
            download_name=f"Bonafide_{student['usn']}.pdf"
        )

    except Exception as e:

        return f"Certificate generation failed: {e}", 500


# --------------------------------------------------
# Verify certificate using QR code
# --------------------------------------------------

@app.route("/verify/<certificate_number>")
def verify_certificate(certificate_number):

    # Expected format:
    # BON-2026-1AB23CS001

    parts = certificate_number.split("-")

    if len(parts) != 3:

        return render_template(
            "verify.html",
            valid=False,
            message="Invalid certificate number."
        )

    usn = parts[2]

    student = find_student_by_usn(usn)

    if student is None:

        return render_template(
            "verify.html",
            valid=False,
            message="Certificate not found in college database."
        )

    return render_template(
        "verify.html",
        valid=True,
        student=student,
        certificate_number=certificate_number
    )


# --------------------------------------------------
# Run Flask
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )