import tkinter as tk
from tkinter import filedialog, messagebox
import difflib
import os

class FileComparator:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Comparator with Diff Viewer")

        self.file1_path = ""
        self.file2_path = ""

        # Buttons
        tk.Button(root, text="Select File 1", command=self.load_file1).pack(pady=5)
        tk.Button(root, text="Select File 2", command=self.load_file2).pack(pady=5)
        tk.Button(root, text="Compare", command=self.compare_files).pack(pady=5)
        tk.Button(root, text="Export Diff Report", command=self.export_diff).pack(pady=5)

        # Frames for side-by-side view
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.text1 = tk.Text(frame, width=80, wrap=tk.NONE)
        self.text1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.text2 = tk.Text(frame, width=80, wrap=tk.NONE)
        self.text2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar sync
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text1.config(yscrollcommand=self.yscroll)
        self.text2.config(yscrollcommand=self.yscroll)

        # Tags for highlighting
        for text in (self.text1, self.text2):
            text.tag_configure("added", background="#ccffcc")
            text.tag_configure("removed", background="#ffcccc")
            text.tag_configure("changed", background="#ffff99")

        self.diff_data = []

    def yview(self, *args):
        self.text1.yview(*args)
        self.text2.yview(*args)

    def yscroll(self, *args):
        self.text1.yview_moveto(args[0])
        self.text2.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def load_file1(self):
        path = filedialog.askopenfilename(title="Select First File")
        if path:
            self.file1_path = path
            messagebox.showinfo("File 1", f"Loaded: {os.path.basename(path)}")

    def load_file2(self):
        path = filedialog.askopenfilename(title="Select Second File")
        if path:
            self.file2_path = path
            messagebox.showinfo("File 2", f"Loaded: {os.path.basename(path)}")

    def compare_files(self):
        if not self.file1_path or not self.file2_path:
            messagebox.showerror("Error", "Please select both files.")
            return

        with open(self.file1_path, "r") as f1, open(self.file2_path, "r") as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        self.text1.delete("1.0", tk.END)
        self.text2.delete("1.0", tk.END)
        self.diff_data = []

        d = difflib.Differ()
        diff = list(d.compare(lines1, lines2))

        idx1 = idx2 = 1

        for line in diff:
            tag = None
            if line.startswith("  "):
                self.text1.insert(f"{idx1}.0", line[2:])
                self.text2.insert(f"{idx2}.0", line[2:])
                idx1 += 1
                idx2 += 1
            elif line.startswith("- "):
                self.text1.insert(f"{idx1}.0", line[2:], "removed")
                self.text2.insert(f"{idx2}.0", "\n")
                idx1 += 1
            elif line.startswith("+ "):
                self.text1.insert(f"{idx1}.0", "\n")
                self.text2.insert(f"{idx2}.0", line[2:], "added")
                idx2 += 1
            elif line.startswith("? "):
                # Show hint line in yellow
                self.text1.insert(f"{idx1}.0", line[2:], "changed")
                self.text2.insert(f"{idx2}.0", line[2:], "changed")
                idx1 += 1
                idx2 += 1

            self.diff_data.append(line)

    def export_diff(self):
        if not self.diff_data:
            messagebox.showwarning("Warning", "No comparison data to export.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Save Diff Report"
        )
        if path:
            with open(path, "w") as f:
                f.writelines(self.diff_data)
            messagebox.showinfo("Exported", f"Diff report saved to:\n{path}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = FileComparator(root)
    root.mainloop()
