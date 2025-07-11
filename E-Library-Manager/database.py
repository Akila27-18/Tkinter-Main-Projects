import sqlite3
from datetime import datetime

def get_connection():
    return sqlite3.connect("library.db")

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre_id INTEGER,
            author_id INTEGER,
            is_issued INTEGER DEFAULT 0,
            FOREIGN KEY (genre_id) REFERENCES genres(id),
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            student_name TEXT,
            issue_date TEXT,
            return_date TEXT,
            fine REAL DEFAULT 0,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')

    conn.commit()
    conn.close()
