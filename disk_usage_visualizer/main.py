import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from collections import defaultdict
import humanize

class DiskUsageVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Usage Visualizer")
        self.root.geometry("900x600")

        self.folder_data = {}
        self.largest_files = []

        self.create_widgets()

    def create_widgets(self):
        # Frame for controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Select Folder", command=self.select_folder).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Export CSV", command=self.export_csv).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Export PNG", command=self.export_png).pack(side=tk.LEFT, padx=10)

        # Treeview for largest files
        self.tree = ttk.Treeview(self.root, columns=("File", "Size"), show="headings")
        self.tree.heading("File", text="File")
        self.tree.heading("Size", text="Size")
        self.tree.column("File", width=500)
        self.tree.column("Size", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Matplotlib figure for pie chart
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.analyze_folder(path)

    def analyze_folder(self, path):
        self.folder_data = defaultdict(int)
        self.largest_files = []

        for root, dirs, files in os.walk(path):
            total_folder_size = 0
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    total_folder_size += size
                    self.largest_files.append((file_path, size))
                except Exception as e:
                    print(f"Error: {e}")
            self.folder_data[root] += total_folder_size

        # Sort and keep top 10 largest files
        self.largest_files.sort(key=lambda x: x[1], reverse=True)
        self.largest_files = self.largest_files[:10]

        self.update_treeview()
        self.plot_pie_chart()

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for filepath, size in self.largest_files:
            self.tree.insert("", tk.END, values=(filepath, humanize.naturalsize(size)))

    def plot_pie_chart(self):
        self.ax.clear()

        folders = list(self.folder_data.keys())
        sizes = list(self.folder_data.values())

        if not sizes or sum(sizes) == 0:
            self.ax.set_title("No data to display")
        else:
            # Limit chart to top 10 by size
            combined = sorted(zip(folders, sizes), key=lambda x: x[1], reverse=True)
            top_folders = combined[:10]
            other_size = sum(s[1] for s in combined[10:])
            if other_size > 0:
                top_folders.append(("Other", other_size))

            labels = [os.path.basename(folder) or folder for folder, _ in top_folders]
            chart_sizes = [size for _, size in top_folders]

            self.ax.pie(chart_sizes, labels=labels, autopct="%1.1f%%", startangle=140)
            self.ax.set_title("Disk Usage (Top Folders)")

        self.canvas.draw()

    def export_csv(self):
        if not self.folder_data:
            messagebox.showwarning("No Data", "Please analyze a folder first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                with open(file_path, "w", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Folder", "Size (Bytes)", "Size (Readable)"])
                    for folder, size in self.folder_data.items():
                        writer.writerow([folder, size, humanize.naturalsize(size)])
                messagebox.showinfo("Exported", f"Report saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def export_png(self):
        if not self.folder_data:
            messagebox.showwarning("No Data", "Please analyze a folder first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png")])
        if file_path:
            try:
                self.fig.savefig(file_path)
                messagebox.showinfo("Exported", f"Chart saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DiskUsageVisualizer(root)
    root.mainloop()
