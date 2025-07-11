import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

def quiz_window(username, category, count):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "quiz.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Get questions for the selected category
    cur.execute("""
        SELECT id, question, option1, option2, option3, option4, answer 
        FROM questions 
        WHERE category = ? 
        ORDER BY RANDOM() 
        LIMIT ?
    """, (category, count))
    questions = cur.fetchall()
    con.close()

    if not questions:
        messagebox.showerror("No Questions", f"No questions available in category '{category}'")
        return

    current_question_index = [0]
    selected_answers = [None] * len(questions)

    def load_question():
        index = current_question_index[0]
        qid, question, op1, op2, op3, op4, correct = questions[index]
        lbl_question.config(text=f"Q{index+1}: {question}")
        options_var.set(None)
        r1.config(text=op1, value=1)
        r2.config(text=op2, value=2)
        r3.config(text=op3, value=3)
        r4.config(text=op4, value=4)
        if selected_answers[index]:
            options_var.set(selected_answers[index])

    def next_question():
        if options_var.get() == 0:
            messagebox.showwarning("No Answer", "Please select an option.")
            return
        selected_answers[current_question_index[0]] = options_var.get()
        if current_question_index[0] < len(questions) - 1:
            current_question_index[0] += 1
            load_question()
        else:
            submit_quiz()

    def previous_question():
        if current_question_index[0] > 0:
            selected_answers[current_question_index[0]] = options_var.get()
            current_question_index[0] -= 1
            load_question()

    def submit_quiz():
        selected_answers[current_question_index[0]] = options_var.get()
        score = 0
        for i, ans in enumerate(selected_answers):
            if ans == questions[i][6]:  # compare with 'answer' from DB
                score += 1

        total = len(questions)
        save_score(username, category, score, total)

        messagebox.showinfo("Quiz Completed", f"Score: {score}/{total}")
        win.destroy()

    def save_score(username, category, score, total):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("INSERT INTO scores (username, category, score, total) VALUES (?, ?, ?, ?)",
                    (username, category, score, total))
        con.commit()
        con.close()

    # GUI Layout
    win = tk.Toplevel()
    win.title(f"Quiz - {category}")
    win.geometry("500x400")

    lbl_question = tk.Label(win, text="", font=("Arial", 14), wraplength=480, justify="left")
    lbl_question.pack(pady=20)

    options_var = tk.IntVar()
    options_var.set(0)

    r1 = tk.Radiobutton(win, text="", variable=options_var, value=1, font=("Arial", 12))
    r1.pack(anchor="w", padx=20)

    r2 = tk.Radiobutton(win, text="", variable=options_var, value=2, font=("Arial", 12))
    r2.pack(anchor="w", padx=20)

    r3 = tk.Radiobutton(win, text="", variable=options_var, value=3, font=("Arial", 12))
    r3.pack(anchor="w", padx=20)

    r4 = tk.Radiobutton(win, text="", variable=options_var, value=4, font=("Arial", 12))
    r4.pack(anchor="w", padx=20)

    nav_frame = tk.Frame(win)
    nav_frame.pack(pady=20)

    btn_prev = tk.Button(nav_frame, text="<< Previous", command=previous_question)
    btn_prev.pack(side="left", padx=10)

    btn_next = tk.Button(nav_frame, text="Next >>", command=next_question)
    btn_next.pack(side="left", padx=10)

    btn_submit = tk.Button(win, text="Submit Quiz", command=submit_quiz, bg="green", fg="white")
    btn_submit.pack(pady=10)

    load_question()
    win.mainloop()


def launch_quiz():
    def start():
        username = entry_name.get().strip()
        category = category_var.get()
        count = int(entry_count.get())

        if not username:
            messagebox.showwarning("Missing Info", "Enter your name.")
            return
        if not category:
            messagebox.showwarning("Missing Info", "Select a category.")
            return
        if count <= 0:
            messagebox.showwarning("Invalid", "Enter a valid number of questions.")
            return

        root.destroy()
        quiz_window(username, category, count)

    # Fetch categories from DB
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "quiz.db")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM categories")
    categories = [row[0] for row in cur.fetchall()]
    con.close()

    root = tk.Tk()
    root.title("Start Quiz")
    root.geometry("400x300")

    tk.Label(root, text="Enter Your Name:").pack(pady=5)
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Label(root, text="Select Category:").pack(pady=5)
    category_var = tk.StringVar()
    category_menu = tk.OptionMenu(root, category_var, *categories)
    category_menu.pack()

    tk.Label(root, text="Number of Questions:").pack(pady=5)
    entry_count = tk.Entry(root)
    entry_count.pack()

    tk.Button(root, text="Start Quiz", command=start, bg="blue", fg="white").pack(pady=20)

    root.mainloop()
