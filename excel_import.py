import sqlite3
import pandas as pd

EXCEL_FILE = "students.xlsx"
DB_NAME = "college.db"


def import_students():
    df = pd.read_excel(EXCEL_FILE)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO students
                (usn, name, course, department, semester, academic_year)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(row["USN"]).strip().upper(),
                str(row["Name"]).strip(),
                str(row["Course"]).strip(),
                str(row["Department"]).strip(),
                str(row["Semester"]).strip(),
                str(row["Academic Year"]).strip()
            ))

        except sqlite3.IntegrityError:
            print(f"Already exists: {row['USN']}")

    conn.commit()
    conn.close()

    print("Excel data imported successfully!")
    print(f"Total students in Excel: {len(df)}")


if __name__ == "__main__":
    import_students()