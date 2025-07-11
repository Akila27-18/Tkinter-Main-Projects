import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3, csv
from db_setup import init_db

def add_question(category, q, o1, o2, o3, o4, correct):
    if not all([category, q, o1, o2, o3, o4, correct]):
        return "All fields are required."
    if correct not in ["1", "2", "3", "4"]:
        return "Correct option must be 1, 2, 3 or 4."
    con = sqlite3.connect("quiz_app/quiz.db")
    con.execute("INSERT OR IGNORE INTO categories(name) VALUES (?)", (category,))
    con.execute("INSERT INTO questions (category, question, option1, option2, option3, option4, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (category, q, o1, o2, o3, o4, int(correct)))
    con.commit()
    con.close()
    return "Question added successfully."

def import_csv(path):
    con = sqlite3.connect("quiz_app/quiz.db")
    cur = con.cursor()
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT OR IGNORE INTO categories(name) VALUES (?)", (row['category'],))
            cur.execute("""INSERT INTO questions (category, question, option1, option2, option3, option4, correct_option)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (row['category'], row['question'], row['option1'], row['option2'], row['option3'], row['option4'], int(row['correct_option'])))
    con.commit()
    con.close()

def export_csv(path):
    con = sqlite3.connect("quiz_app/quiz.db")
    cur = con.cursor()
    rows = cur.execute("SELECT category, question, option1, option2, option3, option4, correct_option FROM questions").fetchall()
    con.close()
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'question', 'option1', 'option2', 'option3', 'option4', 'correct_option'])
        writer.writerows(rows)

def question_manager_ui():
    init_db()
    win = tk.Toplevel()
    win.title("Manage Questions")
    win.geometry("400x400")

    entries = [tk.Entry(win) for _ in range(7)]
    labels = ["Category", "Question", "Option 1", "Option 2", "Option 3", "Option 4", "Correct Option (1-4)"]
    for i, label in enumerate(labels):
        tk.Label(win, text=label).grid(row=i, column=0)
        entries[i].grid(row=i, column=1)

    def on_add():
        values = [e.get() for e in entries]
        msg = add_question(*values)
        messagebox.showinfo("Info", msg)

    def on_import():
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            import_csv(path)
            messagebox.showinfo("Info", "Questions imported.")

    def on_export():
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            export_csv(path)
            messagebox.showinfo("Info", "Questions exported.")

    tk.Button(win, text="Add Question", command=on_add).grid(row=7, columnspan=2, pady=5)
    tk.Button(win, text="Import CSV", command=on_import).grid(row=8, column=0, pady=5)
    tk.Button(win, text="Export CSV", command=on_export).grid(row=8, column=1, pady=5)
