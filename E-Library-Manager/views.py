import tkinter as tk
from tkinter import ttk, messagebox
from book_manager import get_available_books, get_issued_books
from issue_manager import issue_book
from return_manager import return_book
from database import init_db

def launch_ui():
    init_db()
    root = tk.Tk()
    root.title("E-Library Manager")

    tab = ttk.Notebook(root)
    tab.pack(expand=1, fill="both")

    # Available Books
    frame1 = ttk.Frame(tab)
    tab.add(frame1, text="Available Books")
    tree1 = ttk.Treeview(frame1, columns=("ID", "Title", "Author", "Genre"), show="headings")
    for col in ("ID", "Title", "Author", "Genre"):
        tree1.heading(col, text=col)
    tree1.pack(fill="both", expand=True)

    def refresh_available():
        for row in tree1.get_children():
            tree1.delete(row)
        for book in get_available_books():
            tree1.insert("", "end", values=book)

    refresh_available()

    # Issued Books
    frame2 = ttk.Frame(tab)
    tab.add(frame2, text="Issued Books")
    tree2 = ttk.Treeview(frame2, columns=("Title", "Student", "Issued Date"), show="headings")
    for col in ("Title", "Student", "Issued Date"):
        tree2.heading(col, text=col)
    tree2.pack(fill="both", expand=True)

    def refresh_issued():
        for row in tree2.get_children():
            tree2.delete(row)
        for book in get_issued_books():
            tree2.insert("", "end", values=book)

    refresh_issued()

    # Buttons
    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    tk.Label(control_frame, text="Book ID:").grid(row=0, column=0)
    entry_book_id = tk.Entry(control_frame)
    entry_book_id.grid(row=0, column=1)

    tk.Label(control_frame, text="Student Name:").grid(row=0, column=2)
    entry_student = tk.Entry(control_frame)
    entry_student.grid(row=0, column=3)

    def issue_btn():
        try:
            book_id = int(entry_book_id.get())
            student = entry_student.get()
            if not student:
                raise ValueError("Student name required.")
            issue_book(book_id, student)
            messagebox.showinfo("Issued", "Book issued successfully.")
            refresh_available()
            refresh_issued()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def return_btn():
        try:
            book_id = int(entry_book_id.get())
            return_book(book_id)
            messagebox.showinfo("Returned", "Book returned.")
            refresh_available()
            refresh_issued()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(control_frame, text="Issue Book", command=issue_btn).grid(row=0, column=4, padx=5)
    tk.Button(control_frame, text="Return Book", command=return_btn).grid(row=0, column=5, padx=5)

    root.mainloop()
