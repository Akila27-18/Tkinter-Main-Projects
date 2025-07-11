import tkinter as tk
import sqlite3
from db_setup import init_db

def show_leaderboard():
    init_db()
    win = tk.Toplevel()
    win.title("Leaderboard")
    win.geometry("400x300")
    tk.Label(win, text="Top Scores").pack()

    con = sqlite3.connect("quiz_app/quiz.db")
    cur = con.cursor()
    cur.execute("SELECT username, category, score, total, timestamp FROM scores ORDER BY score DESC LIMIT 10")
    rows = cur.fetchall()
    con.close()

    for row in rows:
        tk.Label(win, text=f"{row[0]} ({row[1]}): {row[2]}/{row[3]} at {row[4]}").pack()
