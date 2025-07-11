import sqlite3
import os
from datetime import datetime

DB_NAME = "file_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            action TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_action(filename, action):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO history (filename, action, timestamp) VALUES (?, ?, ?)", 
              (filename, action, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
