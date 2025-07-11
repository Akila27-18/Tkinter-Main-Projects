import sqlite3
import os
from datetime import datetime

DB_PATH = "time_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_task(task, start, end, duration):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task, start_time, end_time, duration) VALUES (?, ?, ?, ?)",
                (task, start, end, duration))
    conn.commit()
    conn.close()

def get_tasks_by_date(date_str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT task, duration FROM tasks WHERE DATE(start_time) = ?", (date_str,))
    results = cur.fetchall()
    conn.close()
    return results

def get_weekly_summary():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT task, SUM(duration) FROM tasks 
        WHERE start_time >= DATE('now', '-6 days') 
        GROUP BY task
    """)
    results = cur.fetchall()
    conn.close()
    return results
