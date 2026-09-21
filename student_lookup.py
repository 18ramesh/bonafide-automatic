import sqlite3

DB_NAME = "college.db"


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


usn = input("Enter Student USN: ")

student = find_student_by_usn(usn)

if student:
    print("\nStudent Found!")
    print("USN:", student["usn"])
    print("Name:", student["name"])
    print("Course:", student["course"])
    print("Department:", student["department"])
    print("Semester:", student["semester"])
    print("Academic Year:", student["academic_year"])
else:
    print("\nStudent not found!")