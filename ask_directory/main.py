import os
import shutil
import threading
from tkinter import Tk, Button, Label, Checkbutton, IntVar, filedialog, Text, END
from datetime import datetime
from collections import defaultdict

# File type mappings
FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.doc', '.docx', '.txt', '.odt'],
    'PDFs': ['.pdf'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
    'Audio': ['.mp3', '.wav', '.aac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Spreadsheets': ['.xls', '.xlsx', '.csv'],
    'Presentations': ['.ppt', '.pptx']
}

# Get category for a file
def get_category(extension):
    for category, exts in FILE_CATEGORIES.items():
        if extension.lower() in exts:
            return category
    return 'Others'

# Create subfolder structure
def get_target_path(base_dir, file_path, use_date_folders):
    ext = os.path.splitext(file_path)[1]
    category = get_category(ext)
    if use_date_folders:
        mod_time = os.path.getmtime(file_path)
        date = datetime.fromtimestamp(mod_time)
        return os.path.join(base_dir, category, str(date.year), date.strftime('%m-%B'))
    else:
        return os.path.join(base_dir, category)

# File organizer function
def organize_files(folder, use_date_folders, log_widget):
    moved_counts = defaultdict(int)
    total_files = 0

    for root, dirs, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isdir(file_path): continue
            rel_path = os.path.relpath(file_path, folder)
            if rel_path.startswith(('.', '_')): continue  # Skip hidden files or system folders

            ext = os.path.splitext(file)[1]
            category = get_category(ext)
            target_dir = get_target_path(folder, file_path, use_date_folders)

            os.makedirs(target_dir, exist_ok=True)
            target_path = os.path.join(target_dir, file)

            # Avoid overwriting
            if os.path.exists(target_path):
                base, ext = os.path.splitext(file)
                i = 1
                while os.path.exists(os.path.join(target_dir, f"{base}_{i}{ext}")):
                    i += 1
                target_path = os.path.join(target_dir, f"{base}_{i}{ext}")

            shutil.move(file_path, target_path)
            moved_counts[category] += 1
            total_files += 1

    log_widget.insert(END, f"\nOrganizing complete. Total files moved: {total_files}\n\n")
    for category, count in moved_counts.items():
        log_widget.insert(END, f"{category}: {count} file(s)\n")
    log_widget.insert(END, "\nDone.\n")

# Multithreaded wrapper
def start_organizing(folder, use_date_folders, log_widget):
    log_widget.delete(1.0, END)
    log_widget.insert(END, f"Organizing folder: {folder}\n")
    threading.Thread(target=organize_files, args=(folder, use_date_folders, log_widget)).start()

# GUI setup
def main():
    root = Tk()
    root.title("File Organizer")
    root.geometry("600x400")

    Label(root, text="Select Folder to Organize", font=("Arial", 12)).pack(pady=10)

    date_folder_var = IntVar()

    def select_folder():
        folder = filedialog.askdirectory()
        if folder:
            start_organizing(folder, date_folder_var.get(), log_output)

    Button(root, text="Choose Folder", command=select_folder, width=20).pack(pady=5)
    Checkbutton(root, text="Sort by Year/Month", variable=date_folder_var).pack(pady=5)

    Label(root, text="Log Output", font=("Arial", 10)).pack(pady=10)
    log_output = Text(root, height=12, width=70)
    log_output.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
