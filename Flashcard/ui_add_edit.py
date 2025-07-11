import tkinter as tk
from tkinter import ttk, messagebox
import database

class AddEditFlashcardUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Add / Edit Flashcards")
        self.setup_ui()
        self.refresh_list()

    def setup_ui(self):
        self.question_var = tk.StringVar()
        self.answer_var = tk.StringVar()

        ttk.Label(self.root, text="Question:").pack()
        ttk.Entry(self.root, textvariable=self.question_var).pack(fill='x')

        ttk.Label(self.root, text="Answer:").pack()
        ttk.Entry(self.root, textvariable=self.answer_var).pack(fill='x')

        ttk.Button(self.root, text="Add Flashcard", command=self.add_flashcard).pack(pady=5)
        ttk.Button(self.root, text="Update Selected", command=self.update_flashcard).pack(pady=5)
        ttk.Button(self.root, text="Delete Selected", command=self.delete_flashcard).pack(pady=5)

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill='both', expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.load_selected)

    def add_flashcard(self):
        q = self.question_var.get().strip()
        a = self.answer_var.get().strip()
        if not q or not a:
            messagebox.showerror("Error", "Fields cannot be empty")
            return
        try:
            database.add_flashcard(q, a)
            self.refresh_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_flashcard(self):
        if not self.listbox.curselection():
            return
        id = self.listbox.get(self.listbox.curselection()).split(" - ")[0]
        q = self.question_var.get().strip()
        a = self.answer_var.get().strip()
        if not q or not a:
            messagebox.showerror("Error", "Fields cannot be empty")
            return
        database.update_flashcard(id, q, a)
        self.refresh_list()

    def delete_flashcard(self):
        if not self.listbox.curselection():
            return
        id = self.listbox.get(self.listbox.curselection()).split(" - ")[0]
        database.delete_flashcard(id)
        self.refresh_list()

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for row in database.get_all_flashcards():
            self.listbox.insert(tk.END, f"{row[0]} - {row[1]}")

    def load_selected(self, e):
        if not self.listbox.curselection():
            return
        id = self.listbox.get(self.listbox.curselection()).split(" - ")[0]
        card = [row for row in database.get_all_flashcards() if str(row[0]) == id][0]
        self.question_var.set(card[1])
        self.answer_var.set(card[2])
