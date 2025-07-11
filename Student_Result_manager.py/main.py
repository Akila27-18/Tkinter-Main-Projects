# main.py
import tkinter as tk
from tkinter import ttk, messagebox
from db import init_db, add_student, fetch_all_students, search_students
from graph_utils import show_individual_result, show_class_average
from export_utils import export_to_csv, export_to_pdf

class ResultApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("950x600")

        self.create_widgets()
        init_db()
        self.load_data()

    def create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Add Student Result")
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Roll No:").grid(row=0, column=0, padx=5, pady=5)
        self.roll_entry = ttk.Entry(input_frame)
        self.roll_entry.grid(row=0, column=1)

        ttk.Label(input_frame, text="Name:").grid(row=0, column=2, padx=5, pady=5)
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=0, column=3)

        self.subject_entries = []
        for i in range(3):
            ttk.Label(input_frame, text=f"Subject {i+1} Marks:").grid(row=1, column=i*2, padx=5, pady=5)
            entry = ttk.Entry(input_frame)
            entry.grid(row=1, column=i*2+1)
            self.subject_entries.append(entry)

        self.add_btn = ttk.Button(input_frame, text="Add Result", command=self.add_result)
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=10)

        # Search
        search_frame = ttk.LabelFrame(self.root, text="Search")
        search_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(search_frame, text="Search by Name or Roll:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left")
        ttk.Button(search_frame, text="Search", command=self.search_student).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Show All", command=self.load_data).pack(side="left")

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("roll", "name", "s1", "s2", "s3", "total", "avg"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Individual Graph", command=self.show_individual_graph).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Class Average Graph", command=self.show_class_graph).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Export CSV", command=export_to_csv).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Export PDF", command=export_to_pdf).pack(side="left", padx=5)

    def add_result(self):
        try:
            roll = self.roll_entry.get().strip()
            name = self.name_entry.get().strip()
            marks = [float(e.get()) for e in self.subject_entries]
            if not roll or not name:
                raise ValueError("Roll no and Name required")
            if not all(0 <= m <= 100 for m in marks):
                raise ValueError("Marks must be between 0-100")
            add_student(roll, name, *marks)
            self.load_data()
            for e in self.subject_entries + [self.roll_entry, self.name_entry]: e.delete(0, 'end')
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in fetch_all_students():
            self.tree.insert("", "end", values=row)

    def search_student(self):
        query = self.search_entry.get().strip()
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in search_students(query):
            self.tree.insert("", "end", values=row)

    def show_individual_graph(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Select a student from the table.")
            return
        data = self.tree.item(selected[0])['values']
        show_individual_result(data)

    def show_class_graph(self):
        show_class_average(fetch_all_students())

if __name__ == '__main__':
    root = tk.Tk()
    app = ResultApp(root)
    root.mainloop()