import os
import hashlib
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

class DuplicateFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplicate File Finder")
        self.root.geometry("800x500")

        self.create_widgets()
        self.duplicates = {}

    def create_widgets(self):
        # Folder selection
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Button(frame, text="Choose Folder", command=self.choose_folder).pack(side=tk.LEFT, padx=5)
        self.folder_label = tk.Label(frame, text="No folder selected", width=80, anchor='w')
        self.folder_label.pack(side=tk.LEFT)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=600)
        self.progress.pack(pady=10)

        # Treeview for duplicates
        self.tree = ttk.Treeview(self.root, columns=("Path", "Size"), show="headings", selectmode="extended")
        self.tree.heading("Path", text="File Path")
        self.tree.heading("Size", text="Size (KB)")
        self.tree.column("Path", width=600)
        self.tree.column("Size", width=100, anchor='center')
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Scan for Duplicates", command=self.start_scan).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).pack(side=tk.LEFT, padx=5)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.folder_label.config(text=folder)

    def start_scan(self):
        if not hasattr(self, 'folder_path') or not self.folder_path:
            messagebox.showwarning("Select Folder", "Please choose a folder first.")
            return

        self.tree.delete(*self.tree.get_children())
        self.duplicates.clear()
        self.progress['value'] = 0

        threading.Thread(target=self.scan_duplicates).start()

    def scan_duplicates(self):
        file_hashes = {}
        all_files = []

        # Step 1: Walk directory
        for root, _, files in os.walk(self.folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                if os.path.isfile(filepath):
                    all_files.append(filepath)

        total = len(all_files)
        self.progress['maximum'] = total

        # Step 2: Calculate hashes
        for i, file in enumerate(all_files, 1):
            try:
                file_hash = self.hash_file(file)
                if file_hash in file_hashes:
                    self.duplicates.setdefault(file_hash, []).append(file)
                else:
                    file_hashes[file_hash] = file
            except Exception as e:
                print(f"Error hashing file: {file} - {e}")
            self.progress['value'] = i

        # Step 3: Show duplicates
        for files in self.duplicates.values():
            if len(files) > 1:
                for file in files:
                    size = os.path.getsize(file) // 1024
                    self.tree.insert("", "end", values=(file, size))

        if not self.duplicates:
            messagebox.showinfo("Result", "No duplicate files found.")

    def hash_file(self, path, block_size=65536):
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "No file selected.")
            return

        confirm = messagebox.askyesno("Delete Files", "Are you sure you want to delete selected files?")
        if not confirm:
            return

        for item in selected:
            file_path = self.tree.item(item)['values'][0]
            try:
                os.remove(file_path)
                self.tree.delete(item)
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete file: {file_path}\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DuplicateFinderApp(root)
    root.mainloop()
