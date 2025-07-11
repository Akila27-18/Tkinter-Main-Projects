import sqlite3
from datetime import datetime, timedelta

DB_NAME = "flashcards.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT UNIQUE,
                answer TEXT,
                interval INTEGER DEFAULT 1,
                due_date TEXT
            )
        ''')
        conn.commit()

def add_flashcard(question, answer):
    with get_connection() as conn:
        due_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        conn.execute("INSERT INTO flashcards (question, answer, due_date) VALUES (?, ?, ?)", (question, answer, due_date))
        conn.commit()

def update_flashcard(id, question, answer):
    with get_connection() as conn:
        conn.execute("UPDATE flashcards SET question=?, answer=? WHERE id=?", (question, answer, id))
        conn.commit()

def delete_flashcard(id):
    with get_connection() as conn:
        conn.execute("DELETE FROM flashcards WHERE id=?", (id,))
        conn.commit()

def get_all_flashcards():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM flashcards").fetchall()

def get_due_flashcards():
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        return conn.execute("SELECT * FROM flashcards WHERE due_date <= ?", (today,)).fetchall()

def update_review(id, difficulty):
    days = {"Easy": 7, "Medium": 3, "Hard": 1}.get(difficulty, 1)
    next_due = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute("UPDATE flashcards SET due_date=?, interval=? WHERE id=?", (next_due, days, id))
        conn.commit()

# Initialize DB
init_db()
