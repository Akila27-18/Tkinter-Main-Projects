import tkinter as tk
from tkinter import ttk, messagebox
from ui_add_edit import AddEditFlashcardUI
from ui_review import ReviewUI
from charts import show_stats

def main():
    root = tk.Tk()
    root.title("Flashcard Learning Tool")

    def open_add_edit():
        AddEditFlashcardUI(tk.Toplevel(root))

    def open_review():
        ReviewUI(tk.Toplevel(root))

    def open_stats():
        show_stats()

    ttk.Button(root, text="Add / Edit Flashcards", command=open_add_edit).pack(padx=20, pady=10)
    ttk.Button(root, text="Review Flashcards", command=open_review).pack(padx=20, pady=10)
    ttk.Button(root, text="View Progress Stats", command=open_stats).pack(padx=20, pady=10)
    ttk.Button(root, text="Exit", command=root.destroy).pack(padx=20, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
