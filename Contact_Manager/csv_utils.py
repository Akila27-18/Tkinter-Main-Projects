
import csv
from tkinter import filedialog, messagebox
from database import add_contact, get_all_contacts

def import_contacts_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 5:
                    add_contact(tuple(row))
        messagebox.showinfo("Success", "Contacts imported successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def export_contacts_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        contacts = get_all_contacts()
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows([c[1:] for c in contacts])
        messagebox.showinfo("Success", "Contacts exported successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
