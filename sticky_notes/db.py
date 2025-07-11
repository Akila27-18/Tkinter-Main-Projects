import sqlite3
import os
from datetime import datetime

DB_PATH = "notes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            x INTEGER,
            y INTEGER,
            color TEXT,
            reminder TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_note(content, x, y, color, reminder, note_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if note_id:
        c.execute('''
            UPDATE notes SET content=?, x=?, y=?, color=?, reminder=? WHERE id=?
        ''', (content, x, y, color, reminder, note_id))
    else:
        c.execute('''
            INSERT INTO notes (content, x, y, color, reminder) VALUES (?, ?, ?, ?, ?)
        ''', (content, x, y, color, reminder))
        note_id = c.lastrowid
    conn.commit()
    conn.close()
    return note_id

def delete_note(note_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM notes WHERE id=?', (note_id,))
    conn.commit()
    conn.close()

def get_all_notes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    notes = c.fetchall()
    conn.close()
    return notes
