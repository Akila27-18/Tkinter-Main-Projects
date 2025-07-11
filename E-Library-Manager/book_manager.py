import sqlite3
from database import get_connection

def add_book(title, genre_id, author_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO books (title, genre_id, author_id) VALUES (?, ?, ?)", (title, genre_id, author_id))
    conn.commit()
    conn.close()

def get_available_books():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT books.id, books.title, authors.name, genres.name FROM books
        JOIN authors ON books.author_id = authors.id
        JOIN genres ON books.genre_id = genres.id
        WHERE is_issued = 0
    ''')
    return c.fetchall()

def get_issued_books():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT books.title, issues.student_name, issues.issue_date FROM issues
        JOIN books ON books.id = issues.book_id
        WHERE issues.return_date IS NULL
    ''')
    return c.fetchall()
