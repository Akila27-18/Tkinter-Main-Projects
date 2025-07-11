# export_utils.py
import csv
from tkinter import filedialog, messagebox
import sqlite3

DB_NAME = "invoices.db"

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()
    conn.close()

    headers = [description[0] for description in cursor.description]
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        messagebox.showinfo("Exported", f"Invoices exported as CSV:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export CSV:\n{e}")

def export_to_txt():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices")
    rows = cursor.fetchall()
    conn.close()

    headers = [description[0] for description in cursor.description]
    try:
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write("\t".join(headers) + "\n")
            for row in rows:
                f.write("\t".join(str(item) for item in row) + "\n")
        messagebox.showinfo("Exported", f"Invoices exported as TXT:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export TXT:\n{e}")
