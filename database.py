import sqlite3

DB_NAME = "college.db"

def create_database():
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
    conn.close()

    print("Database created successfully!")

if __name__ == "__main__":
    create_database()