import sqlite3

def init_db():
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            tags TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_note(note_id, title, tags, content):
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()
    if note_id:
        cur.execute("UPDATE notes SET title=?, tags=?, content=? WHERE id=?", (title, tags, content, note_id))
    else:
        cur.execute("INSERT INTO notes (title, tags, content) VALUES (?, ?, ?)", (title, tags, content))
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cur.fetchall()
    conn.close()
    return notes

def search_notes(query):
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE title LIKE ? OR tags LIKE ?", (f'%{query}%', f'%{query}%'))
    notes = cur.fetchall()
    conn.close()
    return notes

def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
