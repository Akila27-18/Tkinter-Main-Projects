import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from preview_pane import MarkdownPreview
from export_utils import export_to_txt, export_to_pdf
from db import init_db, save_note, get_notes, search_notes, delete_note

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Note-taking App")
        self.create_widgets()
        init_db()
        self.load_notes()

    def create_widgets(self):
        # Top Frame for title and tags
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(top_frame, text="Title:").grid(row=0, column=0, sticky='w')
        self.title_entry = ttk.Entry(top_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5)

        ttk.Label(top_frame, text="Tags (comma):").grid(row=0, column=2, sticky='w')
        self.tag_entry = ttk.Entry(top_frame, width=30)
        self.tag_entry.grid(row=0, column=3)

        # Main Frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left: Note list and search
        left_frame = ttk.Frame(main_frame, width=200)
        left_frame.pack(side='left', fill='y')

        self.search_var = tk.StringVar()
        ttk.Entry(left_frame, textvariable=self.search_var).pack(pady=5, fill='x')
        ttk.Button(left_frame, text="Search", command=self.search_notes).pack(fill='x')

        self.note_listbox = tk.Listbox(left_frame)
        self.note_listbox.pack(fill='y', expand=True)
        self.note_listbox.bind('<<ListboxSelect>>', self.load_selected_note)

        # Right: Text editor and preview
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)

        self.text = tk.Text(right_frame, wrap='word', height=20)
        self.text.pack(fill='both', expand=True, side='left')

        self.preview = MarkdownPreview(right_frame)
        self.preview.pack(fill='both', expand=True, side='right')

        self.text.bind('<KeyRelease>', lambda e: self.preview.update_preview(self.text.get("1.0", tk.END)))

        # Bottom: Buttons
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(bottom_frame, text="Save", command=self.save_current_note).pack(side='left')
        ttk.Button(bottom_frame, text="Delete", command=self.delete_current_note).pack(side='left')
        ttk.Button(bottom_frame, text="Export as TXT", command=lambda: export_to_txt(self.title_entry.get(), self.text.get("1.0", tk.END))).pack(side='right')
        ttk.Button(bottom_frame, text="Export as PDF", command=lambda: export_to_pdf(self.title_entry.get(), self.text.get("1.0", tk.END))).pack(side='right')

    def load_notes(self):
        self.note_listbox.delete(0, tk.END)
        self.notes = get_notes()
        for note in self.notes:
            self.note_listbox.insert(tk.END, note[1])  # Title

    def load_selected_note(self, event):
        selection = self.note_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        note = self.notes[index]
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note[1])
        self.tag_entry.delete(0, tk.END)
        self.tag_entry.insert(0, note[2])
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, note[3])
        self.preview.update_preview(note[3])
        self.current_note_id = note[0]

    def save_current_note(self):
        title = self.title_entry.get().strip()
        tags = self.tag_entry.get().strip()
        content = self.text.get("1.0", tk.END).strip()
        if not title or not content:
            messagebox.showerror("Error", "Title and content are required.")
            return
        note_id = getattr(self, 'current_note_id', None)
        save_note(note_id, title, tags, content)
        self.load_notes()
        self.title_entry.delete(0, tk.END)
        self.tag_entry.delete(0, tk.END)
        self.text.delete("1.0", tk.END)
        self.preview.update_preview("")

    def search_notes(self):
        query = self.search_var.get().strip()
        if not query:
            self.load_notes()
            return
        self.notes = search_notes(query)
        self.note_listbox.delete(0, tk.END)
        for note in self.notes:
            self.note_listbox.insert(tk.END, note[1])

    def delete_current_note(self):
        if hasattr(self, 'current_note_id'):
            delete_note(self.current_note_id)
            self.load_notes()
            self.title_entry.delete(0, tk.END)
            self.tag_entry.delete(0, tk.END)
            self.text.delete("1.0", tk.END)
            self.preview.update_preview("")

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
