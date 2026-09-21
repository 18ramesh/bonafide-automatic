from flask import Flask, render_template, request, send_file
import sqlite3

from pdf_generator import generate_bonafide


app = Flask(__name__)

DB_NAME = "college.db"


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
        port=5000,
        debug=True
    )