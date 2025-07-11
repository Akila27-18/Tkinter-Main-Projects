
import tkinter as tk
from tkinter import messagebox
import sqlite3
import threading
import time

class ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Exam Simulator")
        self.db = sqlite3.connect("exam.db")
        self.cursor = self.db.cursor()
        self.create_tables()
        self.current_question = 0
        self.score = 0
        self.negative = 0.25
        self.answers = []
        self.user_answers = []
        self.timer_running = False
        self.time_left = 300

        self.load_questions()
        self.build_gui()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question TEXT,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            answer INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            name TEXT,
            score REAL)''')
        self.db.commit()

    def load_questions(self):
        self.cursor.execute("SELECT * FROM questions")
        self.questions = self.cursor.fetchall()
        if not self.questions:
            default_qs = [
                ("Capital of India?", "Mumbai", "Delhi", "Kolkata", "Chennai", 2),
                ("2 + 2 = ?", "3", "4", "5", "6", 2),
                ("Sun rises in the?", "North", "South", "East", "West", 3)
            ]
            for q in default_qs:
                self.cursor.execute("INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)", q)
            self.db.commit()
            self.cursor.execute("SELECT * FROM questions")
            self.questions = self.cursor.fetchall()

    def build_gui(self):
        self.name_var = tk.StringVar()
        self.timer_label = tk.Label(self.root, text="Time: 05:00", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        tk.Label(self.root, text="Enter Your Name:").pack()
        self.name_entry = tk.Entry(self.root, textvariable=self.name_var)
        self.name_entry.pack(pady=5)

        self.q_frame = tk.Frame(self.root)
        self.q_frame.pack(pady=10)

        self.options = []
        self.opt_var = tk.IntVar()

        self.q_label = tk.Label(self.q_frame, text="", font=("Arial", 14))
        self.q_label.pack()

        for i in range(4):
            rb = tk.Radiobutton(self.q_frame, text="", variable=self.opt_var, value=i+1, font=("Arial", 12))
            rb.pack(anchor="w")
            self.options.append(rb)

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.next_btn = tk.Button(self.btn_frame, text="Next", command=self.next_question)
        self.next_btn.grid(row=0, column=0, padx=5)
        self.submit_btn = tk.Button(self.btn_frame, text="Submit", command=self.submit_exam)
        self.submit_btn.grid(row=0, column=1, padx=5)
        self.reset_btn = tk.Button(self.btn_frame, text="Reset", command=self.reset_exam)
        self.reset_btn.grid(row=0, column=2, padx=5)
        self.start_btn = tk.Button(self.btn_frame, text="Start Exam", command=self.start_timer)
        self.start_btn.grid(row=0, column=3, padx=5)

        self.display_question()

    def start_timer(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Validation Error", "Name is required to start the exam.")
            return

        if not self.timer_running:
            self.timer_running = True
            threading.Thread(target=self.update_timer, daemon=True).start()

    def update_timer(self):
        while self.time_left > 0 and self.timer_running:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"Time: {mins:02}:{secs:02}")
            time.sleep(1)
            self.time_left -= 1
        if self.time_left <= 0:
            messagebox.showinfo("Time Up", "Time is over. Submitting exam.")
            self.submit_exam()

    def display_question(self):
        if self.current_question < len(self.questions):
            q = self.questions[self.current_question]
            self.q_label.config(text=q[1])
            for i in range(4):
                self.options[i].config(text=q[i+2])
            self.opt_var.set(0)
        else:
            self.submit_exam()

    def next_question(self):
        selected = self.opt_var.get()
        if selected == 0:
            messagebox.showwarning("Warning", "Please select an option.")
            return
        self.user_answers.append(selected)
        self.current_question += 1
        self.display_question()

    def submit_exam(self):
        self.timer_running = False
        while len(self.user_answers) < len(self.questions):
            self.user_answers.append(0)
        correct = 0
        for i, q in enumerate(self.questions):
            if self.user_answers[i] == q[6]:
                correct += 1
            elif self.user_answers[i] != 0:
                correct -= self.negative

        score = max(0, round(correct, 2))
        self.cursor.execute("INSERT INTO results (name, score) VALUES (?, ?)", (self.name_var.get(), score))
        self.db.commit()
        messagebox.showinfo("Result", f"Your Score: {score}/{len(self.questions)}")
        self.review_answers()

    def review_answers(self):
        review = tk.Toplevel(self.root)
        review.title("Review Answers")
        for i, q in enumerate(self.questions):
            tk.Label(review, text=f"Q{i+1}: {q[1]}", font=("Arial", 12, "bold")).pack(anchor="w")
            for j in range(4):
                opt_text = q[j+2]
                status = ""
                if self.user_answers[i] == j+1:
                    if self.user_answers[i] == q[6]:
                        status = "✅"
                    else:
                        status = "❌"
                elif q[6] == j+1:
                    status = "✔️"
                tk.Label(review, text=f"{j+1}. {opt_text} {status}").pack(anchor="w")

    def reset_exam(self):
        self.current_question = 0
        self.user_answers = []
        self.score = 0
        self.time_left = 300
        self.timer_label.config(text="Time: 05:00")
        self.timer_running = False
        self.display_question()
