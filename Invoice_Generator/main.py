# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import init_db, insert_invoice, get_filtered_invoices
from invoice_logic import (
    generate_invoice_number, validate_invoice_fields,
    calculate_totals, get_current_datetime
)
from export_pdf import export_invoice_to_pdf
from export_utils import export_to_csv, export_to_txt
from styles import apply_dark_theme

init_db()

# --- MAIN WINDOW ---
root = tk.Tk()
root.title("Invoice Generator")
root.geometry("1000x600")

# --- SIDEBAR ---
sidebar = tk.Frame(root, width=180, bg="#2b2b3d")
sidebar.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(sidebar, text="Business Tools", fg="white", bg="#2b2b3d", font=("Segoe UI", 14, "bold")).pack(pady=20)

btn_invoice = tk.Button(sidebar, text="New Invoice", width=20)
btn_invoice.pack(pady=10)
btn_export_csv = tk.Button(sidebar, text="Export CSV", width=20, command=export_to_csv)
btn_export_csv.pack(pady=5)
btn_export_txt = tk.Button(sidebar, text="Export TXT", width=20, command=export_to_txt)
btn_export_txt.pack(pady=5)

# --- MAIN CONTENT AREA ---
main_frame = tk.Frame(root, bg="#1e1e2f")
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# --- FORM ---
form_frame = tk.LabelFrame(main_frame, text="Create New Invoice", padx=10, pady=10)
form_frame.pack(fill="x", padx=20, pady=10)

labels = ["Client Name", "Product/Service", "Quantity", "Unit Price"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(form_frame, text=label).grid(row=i//2, column=(i%2)*2, sticky="e")
    entry = tk.Entry(form_frame, width=30)
    entry.grid(row=i//2, column=(i%2)*2 + 1, padx=10, pady=5)
    entries[label] = entry

def clear_form():
    for e in entries.values():
        e.delete(0, tk.END)

def save_invoice():
    client = entries["Client Name"].get()
    product = entries["Product/Service"].get()
    qty = entries["Quantity"].get()
    price = entries["Unit Price"].get()

    errors = validate_invoice_fields(client, product, qty, price)
    if errors:
        messagebox.showerror("Validation Failed", "\n".join(errors))
        return

    qty = int(qty)
    price = float(price)
    subtotal, tax, total = calculate_totals(qty, price)
    date = get_current_datetime()
    invoice_no = generate_invoice_number()

    data = (invoice_no, date, client, product, qty, price, subtotal, tax, total)
    insert_invoice(data)
    messagebox.showinfo("Success", f"Invoice {invoice_no} saved.")
    clear_form()
    update_treeview()

tk.Button(form_frame, text="Save Invoice", command=save_invoice, bg="#4caf50", fg="white").grid(row=2, column=1, pady=10)
tk.Button(form_frame, text="Clear", command=clear_form).grid(row=2, column=3)

# --- FILTER & TREEVIEW ---
filter_frame = tk.Frame(main_frame, bg="#1e1e2f")
filter_frame.pack(fill="x", padx=20)

tk.Label(filter_frame, text="Filter by Client:", bg="#1e1e2f", fg="white").pack(side=tk.LEFT)
client_filter = tk.Entry(filter_frame)
client_filter.pack(side=tk.LEFT, padx=5)

tk.Label(filter_frame, text="Date (YYYY-MM-DD):", bg="#1e1e2f", fg="white").pack(side=tk.LEFT)
date_filter = tk.Entry(filter_frame)
date_filter.pack(side=tk.LEFT, padx=5)

def update_treeview():
    for row in tree.get_children():
        tree.delete(row)
    results = get_filtered_invoices(client_filter.get(), date_filter.get())
    for r in results:
        tree.insert("", "end", values=r)

tk.Button(filter_frame, text="Filter", command=update_treeview).pack(side=tk.LEFT, padx=10)

tree_frame = tk.Frame(main_frame)
tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

cols = ["Invoice No", "Date", "Client", "Total"]
tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True)

# --- EXPORT / PRINT BUTTONS ---
btns_frame = tk.Frame(main_frame, bg="#1e1e2f")
btns_frame.pack(fill="x", padx=20, pady=5)

def export_selected_pdf():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an invoice to export.")
        return
    invoice_no = tree.item(selected)['values'][0]
    export_invoice_to_pdf(invoice_no)

def print_invoice():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an invoice to print.")
        return
    invoice_no = tree.item(selected)['values'][0]
    export_invoice_to_pdf(invoice_no)
    messagebox.showinfo("Print", "Use system print dialog to print the exported PDF.")

tk.Button(btns_frame, text="Export PDF", command=export_selected_pdf, bg="#2196f3", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(btns_frame, text="Print", command=print_invoice, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)

# --- Apply Theme & Init ---
apply_dark_theme(root)
update_treeview()

root.mainloop()
