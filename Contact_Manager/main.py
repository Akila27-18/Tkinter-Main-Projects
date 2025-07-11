
import tkinter as tk
from tkinter import ttk, messagebox
from database import *
from logic import validate_contact
from email_sender import send_email
from csv_utils import import_contacts_from_csv, export_contacts_to_csv
from styles import apply_dark_theme

init_db()

root = tk.Tk()
root.title("Client Contact Manager")
root.geometry("1000x600")

# --- Top Frame: Form ---
form = tk.LabelFrame(root, text="Contact Details")
form.pack(fill="x", padx=10, pady=10)

labels = ["Name", "Phone", "Email", "Address", "Notes"]
entries = {}
for i, label in enumerate(labels):
    tk.Label(form, text=label).grid(row=i, column=0, sticky="e")
    entry = tk.Entry(form, width=50)
    entry.grid(row=i, column=1, padx=5, pady=3)
    entries[label] = entry

selected_id = None

def clear_form():
    global selected_id
    selected_id = None
    for e in entries.values():
        e.delete(0, tk.END)

def save_contact():
    global selected_id
    values = [entries[l].get() for l in labels]
    errors = validate_contact(values[0], values[1], values[2])
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return
    if selected_id:
        update_contact(selected_id, values)
    else:
        add_contact(values)
    load_contacts()
    clear_form()

def on_select(event):
    global selected_id
    item = tree.focus()
    if not item: return
    values = tree.item(item)["values"]
    selected_id = values[0]
    for i, l in enumerate(labels):
        entries[l].delete(0, tk.END)
        entries[l].insert(0, values[i+1])

def delete_selected():
    global selected_id
    if selected_id:
        delete_contact(selected_id)
        load_contacts()
        clear_form()

# --- Buttons ---
btn_frame = tk.Frame(root)
btn_frame.pack()
tk.Button(btn_frame, text="Save", command=save_contact).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_selected).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_form).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Import CSV", command=import_contacts_from_csv).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Export CSV", command=export_contacts_to_csv).pack(side=tk.LEFT, padx=5)

# --- Search ---
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Go", command=lambda: load_contacts(search_entry.get())).pack(side=tk.LEFT)

# --- Table ---
tree = ttk.Treeview(root, columns=["ID"] + labels, show="headings")
for col in ["ID"] + labels:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True, padx=10, pady=10)
tree.bind("<<TreeviewSelect>>", on_select)

def load_contacts(query=""):
    for row in tree.get_children():
        tree.delete(row)
    rows = search_contacts(query) if query else get_all_contacts()
    for row in rows:
        tree.insert("", "end", values=row)

# --- Email Sender ---
email_frame = tk.LabelFrame(root, text="Send Email")
email_frame.pack(fill="x", padx=10, pady=5)

tk.Label(email_frame, text="From Email:").grid(row=0, column=0)
sender_entry = tk.Entry(email_frame, width=40)
sender_entry.grid(row=0, column=1)

tk.Label(email_frame, text="Password:").grid(row=1, column=0)
password_entry = tk.Entry(email_frame, show="*", width=40)
password_entry.grid(row=1, column=1)

tk.Label(email_frame, text="Subject:").grid(row=2, column=0)
subject_entry = tk.Entry(email_frame, width=60)
subject_entry.grid(row=2, column=1)

tk.Label(email_frame, text="Message:").grid(row=3, column=0)
msg_entry = tk.Text(email_frame, height=5, width=60)
msg_entry.grid(row=3, column=1)

tk.Label(email_frame, text="To Email:").grid(row=4, column=0)
to_entry = tk.Entry(email_frame, width=40)
to_entry.grid(row=4, column=1)

def send_email_click():
    status, msg = send_email(
        sender_entry.get(),
        password_entry.get(),
        to_entry.get(),
        subject_entry.get(),
        msg_entry.get("1.0", "end").strip()
    )
    if status:
        messagebox.showinfo("Success", msg)
    else:
        messagebox.showerror("Failed", msg)

tk.Button(email_frame, text="Send Email", command=send_email_click).grid(row=5, column=1, pady=5, sticky="e")

apply_dark_theme(root)
load_contacts()
root.mainloop()
