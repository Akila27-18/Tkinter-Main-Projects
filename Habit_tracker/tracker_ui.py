import tkinter as tk
from tkinter import messagebox
from database import get_habits, add_habit, log_habit, get_log
from datetime import date, timedelta
from stats import show_stats
from notifier import daily_popup

def launch_app():
    root = tk.Tk()
    root.title("Habit Tracker")

    tk.Label(root, text="Enter Habit Name:").grid(row=0, column=0)
    habit_entry = tk.Entry(root)
    habit_entry.grid(row=0, column=1)

    def add():
        name = habit_entry.get().strip()
        if name:
            add_habit(name)
            refresh()
        else:
            messagebox.showerror("Error", "Habit name required")

    tk.Button(root, text="Add Habit", command=add).grid(row=0, column=2)

    canvas = tk.Canvas(root)
    canvas.grid(row=1, column=0, columnspan=3)

    def refresh():
        for widget in canvas.winfo_children():
            widget.destroy()

        habits = get_habits()
        today = date.today()
        for i, (habit_id, name) in enumerate(habits):
            tk.Label(canvas, text=name).grid(row=i, column=0)
            for j in range(7):
                d = today - timedelta(days=6-j)
                d_str = d.isoformat()
                log = get_log(habit_id)
                var = tk.IntVar(value=1 if (d_str, 1) in log else 0)
                cb = tk.Checkbutton(canvas, variable=var, command=lambda v=var, h=habit_id, ds=d_str: log_habit(h, ds, v.get()))
                cb.grid(row=i, column=j+1)

        tk.Button(canvas, text="Show Stats", command=show_stats).grid(row=len(habits)+1, column=0, columnspan=3)

    refresh()
    daily_popup()
    root.mainloop()
