import sqlite3, os
from datetime import date

DB_NAME = "habit_data.db"

def init_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS habit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date TEXT,
        done INTEGER DEFAULT 0,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
    )''')
    con.commit()
    con.close()

def add_habit(name):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO habits (name) VALUES (?)", (name,))
    con.commit()
    con.close()

def log_habit(habit_id, day, done):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('''INSERT OR REPLACE INTO habit_log (habit_id, date, done)
                   VALUES (?, ?, ?)''', (habit_id, day, done))
    con.commit()
    con.close()

def get_habits():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM habits")
    habits = cur.fetchall()
    con.close()
    return habits

def get_log(habit_id):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("SELECT date, done FROM habit_log WHERE habit_id = ?", (habit_id,))
    logs = cur.fetchall()
    con.close()
    return logs
