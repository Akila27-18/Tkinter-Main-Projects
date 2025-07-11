
import tkinter as tk
from tkinter import ttk, messagebox
from calendar_widget import create_datetime_picker
from scheduler import schedule_reminder
from styles import apply_dark_theme
from datetime import datetime

root = tk.Tk()
root.title("Task Scheduler with Reminders")
root.geometry("800x500")

tasks = []

# --- Task Form ---
form_frame = tk.LabelFrame(root, text="Add New Task", padx=10, pady=10)
form_frame.pack(fill="x", padx=10, pady=10)

tk.Label(form_frame, text="Task Title:").grid(row=0, column=0, sticky="e")
title_entry = tk.Entry(form_frame, width=40)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="e")
desc_entry = tk.Entry(form_frame, width=40)
desc_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Due Date & Time:").grid(row=2, column=0, sticky="e")
date_picker, hour_box, min_box = create_datetime_picker(form_frame)
date_picker.grid(row=2, column=1, sticky="w")
hour_box.grid(row=2, column=1, padx=(110, 0), sticky="w")
min_box.grid(row=2, column=1, padx=(160, 0), sticky="w")

# --- Treeview ---
tree_frame = tk.LabelFrame(root, text="Upcoming Tasks")
tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Title", "Description", "Due")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True)

def add_task():
    title = title_entry.get().strip()
    desc = desc_entry.get().strip()
    date = date_picker.get_date().strftime("%Y-%m-%d")
    hour = hour_box.get()
    minute = min_box.get()

    if not title:
        messagebox.showerror("Validation Error", "Task title is required.")
        return
    if not hour.isdigit() or not minute.isdigit():
        messagebox.showerror("Validation Error", "Invalid time format.")
        return

    dt_str = f"{date} {hour}:{minute}"
    try:
        due_time = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        if due_time < datetime.now():
            raise ValueError("Cannot schedule past time.")
    except Exception as e:
        messagebox.showerror("Validation Error", f"Invalid due time: {e}")
        return

    task = {"title": title, "description": desc, "datetime": dt_str}
    tasks.append(task)
    tree.insert("", "end", values=(title, desc, dt_str))
    schedule_reminder(task, root)
    clear_form()

def clear_form():
    title_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    hour_box.set("09")
    min_box.set("00")

tk.Button(form_frame, text="Add Task", command=add_task).grid(row=3, column=1, pady=10, sticky="e")

apply_dark_theme(root)
root.mainloop()
