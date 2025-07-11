# db.py
import sqlite3

def init_db():
    conn = sqlite3.connect("results.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            sub1 REAL,
            sub2 REAL,
            sub3 REAL,
            total REAL,
            avg REAL
        )
    """)
    conn.commit()
    conn.close()

def add_student(roll, name, s1, s2, s3):
    total = s1 + s2 + s3
    avg = total / 3
    conn = sqlite3.connect("results.db")
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?, ?, ?)",
                (roll, name, s1, s2, s3, total, avg))
    conn.commit()
    conn.close()

def fetch_all_students():
    conn = sqlite3.connect("results.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_students(query):
    conn = sqlite3.connect("results.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE roll LIKE ? OR name LIKE ?",
                (f"%{query}%", f"%{query}%"))
    rows = cur.fetchall()
    conn.close()
    return rows