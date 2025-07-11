import tkinter as tk
from tkinter import messagebox
from database import init_db, insert_task
from utils import get_current_time, time_diff_minutes
from idle_detector import IdleDetector
import report

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")

        self.task = tk.StringVar()
        self.timer_running = False
        self.start_time = None

        tk.Label(root, text="Task:").pack(pady=5)
        tk.Entry(root, textvariable=self.task).pack(pady=5)

        self.start_btn = tk.Button(root, text="Start", command=self.start_timer)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Stop", command=self.stop_timer, state=tk.DISABLED)
        self.stop_btn.pack(pady=5)

        tk.Button(root, text="Show Today's Pie Chart", command=report.show_pie_chart).pack(pady=5)
        tk.Button(root, text="Show Weekly Summary", command=report.show_weekly_summary).pack(pady=5)

        self.idle_detector = IdleDetector(idle_time=60, callback=self.pause_due_to_idle)

        init_db()

    def start_timer(self):
        if not self.task.get():
            messagebox.showwarning("Input Error", "Please enter a task name.")
            return

        self.start_time = get_current_time()
        self.timer_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        print(f"[START] {self.task.get()} at {self.start_time}")

    def stop_timer(self):
        if not self.timer_running:
            return

        end_time = get_current_time()
        duration = time_diff_minutes(self.start_time, end_time)
        insert_task(self.task.get(), self.start_time, end_time, duration)
        print(f"[STOP] {self.task.get()} at {end_time}, duration: {duration} min")

        self.timer_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def pause_due_to_idle(self):
        if self.timer_running:
            self.stop_timer()
            messagebox.showinfo("Idle Detected", "You've been idle. Timer paused automatically.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()
