import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from database import init_db, add_task, get_tasks, update_positions, delete_task
from utils import is_overdue

class TaskItem(tk.Frame):
    def __init__(self, parent, task, refresh_callback):
        super().__init__(parent)
        self.task = task
        self.refresh_callback = refresh_callback
        self.build()

    def build(self):
        bg = "lightcoral" if is_overdue(self.task[5]) else "lightgreen"
        self.configure(bg=bg, bd=1, relief="solid", padx=5, pady=2)

        title = f"{self.task[1]} [{self.task[4]}]"
        tk.Label(self, text=title, bg=bg, font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(self, text=f"{self.task[2]} | Due: {self.task[5]}", bg=bg).pack(anchor="w")

        btn = tk.Button(self, text="Delete", command=self.delete)
        btn.pack(side="right")

    def delete(self):
        delete_task(self.task[0])
        self.refresh_callback()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        root.title("Advanced To-Do List")
        root.geometry("600x600")
        init_db()

        self.build_ui()
        self.refresh_task_list()

    def build_ui(self):
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(pady=10)

        self.title_var = tk.StringVar()
        self.tag_var = tk.StringVar()
        self.priority_var = tk.StringVar()
        self.due_date_var = tk.StringVar()

        tk.Label(self.entry_frame, text="Title").grid(row=0, column=0)
        tk.Entry(self.entry_frame, textvariable=self.title_var).grid(row=0, column=1)

        tk.Label(self.entry_frame, text="Description").grid(row=1, column=0)
        self.desc_entry = tk.Entry(self.entry_frame)
        self.desc_entry.grid(row=1, column=1)

        tk.Label(self.entry_frame, text="Tag").grid(row=2, column=0)
        tk.Entry(self.entry_frame, textvariable=self.tag_var).grid(row=2, column=1)

        tk.Label(self.entry_frame, text="Priority").grid(row=3, column=0)
        ttk.Combobox(self.entry_frame, textvariable=self.priority_var, values=["Low", "Medium", "High"]).grid(row=3, column=1)

        tk.Label(self.entry_frame, text="Due Date (YYYY-MM-DD)").grid(row=4, column=0)
        tk.Entry(self.entry_frame, textvariable=self.due_date_var).grid(row=4, column=1)

        tk.Button(self.entry_frame, text="Add Task", command=self.add_task).grid(row=5, column=0, columnspan=2, pady=5)

        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack()
        self.filter_tag = tk.StringVar()
        tk.Entry(self.filter_frame, textvariable=self.filter_tag, width=20).pack(side="left", padx=5)
        tk.Button(self.filter_frame, text="Filter by Tag", command=self.refresh_task_list).pack(side="left")

        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def add_task(self):
        title = self.title_var.get()
        desc = self.desc_entry.get()
        tag = self.tag_var.get()
        priority = self.priority_var.get()
        due = self.due_date_var.get()

        if not title or not due:
            messagebox.showerror("Validation", "Title and Due Date are required.")
            return

        try:
            datetime.strptime(due, "%Y-%m-%d")
        except:
            messagebox.showerror("Date Error", "Use YYYY-MM-DD format.")
            return

        position = len(get_tasks())
        add_task(title, desc, tag, priority, due, position)
        self.clear_fields()
        self.refresh_task_list()

    def clear_fields(self):
        self.title_var.set("")
        self.desc_entry.delete(0, tk.END)
        self.tag_var.set("")
        self.priority_var.set("")
        self.due_date_var.set("")

    def refresh_task_list(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        tasks = get_tasks(filter_tag=self.filter_tag.get())
        for task in tasks:
            task_item = TaskItem(self.task_frame, task, self.refresh_task_list)
            task_item.pack(fill="x", pady=3)

def launch_app():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
