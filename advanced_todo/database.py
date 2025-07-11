import sqlite3
from datetime import datetime

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

def init_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        tag TEXT,
        priority TEXT,
        due_date TEXT,
        position INTEGER
    )''')
    conn.commit()

def add_task(title, description, tag, priority, due_date, position):
    cursor.execute('''
        INSERT INTO tasks (title, description, tag, priority, due_date, position)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (title, description, tag, priority, due_date, position))
    conn.commit()

def get_tasks(filter_tag=None, due_by=None):
    query = "SELECT * FROM tasks"
    params = []
    if filter_tag:
        query += " WHERE tag = ?"
        params.append(filter_tag)
    elif due_by:
        query += " WHERE due_date <= ?"
        params.append(due_by)
    query += " ORDER BY position ASC"
    cursor.execute(query, params)
    return cursor.fetchall()

def update_positions(task_order):
    for pos, task_id in enumerate(task_order):
        cursor.execute("UPDATE tasks SET position = ? WHERE id = ?", (pos, task_id))
    conn.commit()

def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
