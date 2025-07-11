from quiz_interface import launch_quiz
from question_manager import question_manager_ui
from leaderboard import show_leaderboard
import tkinter as tk

def main_ui():
    root = tk.Tk()
    root.title("Quiz Application")
    root.geometry("300x200")

    tk.Button(root, text="Start Quiz", width=20, command=launch_quiz).pack(pady=10)
    tk.Button(root, text="Manage Questions", width=20, command=question_manager_ui).pack(pady=10)
    tk.Button(root, text="Leaderboard", width=20, command=show_leaderboard).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_ui()
