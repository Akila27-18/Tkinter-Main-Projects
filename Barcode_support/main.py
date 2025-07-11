# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import *
from inventory_logic import *
from export_reports import export_inventory_csv, export_inventory_pdf
from styles import apply_dark_theme, LOW_STOCK_COLOR

init_db()

# --- Main Window ---
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("1100x600")

# --- Product Form ---
form_frame = tk.LabelFrame(root, text="Product Details", padx=10, pady=10)
form_frame.pack(fill="x", padx=15, pady=10)

labels = ["Name", "SKU", "Category", "Price", "Quantity", "Expiry Date"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(form_frame, text=label).grid(row=i//3, column=(i%3)*2, sticky="e")
    entry = tk.Entry(form_frame, width=25)
    entry.grid(row=i//3, column=(i%3)*2 + 1, padx=10, pady=5)
    entries[label] = entry

selected_id = None

def clear_form():
    global selected_id
    for e in entries.values():
        e.delete(0, tk.END)
    selected_id = None

def on_submit():
    global selected_id
    values = [entries[l].get() for l in labels]
    errors = validate_product_fields(*values)
    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))
        return
    if selected_id:  # Update
        update_product(selected_id, values)
        messagebox.showinfo("Updated", "Product updated successfully.")
    else:  # Add new
        try:
            add_product(values)
            messagebox.showinfo("Added", "Product added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product:\n{e}")
    clear_form()
    load_products()

def on_delete():
    global selected_id
    if not selected_id:
        messagebox.showwarning("No Selection", "Select a product to delete.")
        return
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this product?")
    if confirm:
        delete_product(selected_id)
        clear_form()
        load_products()

# --- Buttons ---
btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Save", command=on_submit, bg="#4caf50", fg="white", width=12).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Delete", command=on_delete, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Clear", command=clear_form, width=12).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Export CSV", command=export_inventory_csv, width=12).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Export PDF", command=export_inventory_pdf, width=12).pack(side=tk.LEFT, padx=10)

# --- Search & Barcode Entry ---
search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=15, pady=10)

tk.Label(search_frame, text="Search Name:").pack(side=tk.LEFT)
name_search = tk.Entry(search_frame)
name_search.pack(side=tk.LEFT, padx=5)

tk.Label(search_frame, text="Category:").pack(side=tk.LEFT)
cat_search = tk.Entry(search_frame)
cat_search.pack(side=tk.LEFT, padx=5)

tk.Label(search_frame, text="Scan SKU:").pack(side=tk.LEFT)
sku_input = tk.Entry(search_frame, width=20)
sku_input.pack(side=tk.LEFT, padx=10)

def load_products():
    for row in tree.get_children():
        tree.delete(row)
    records = search_products(name_search.get(), cat_search.get())
    for r in records:
        tags = ("low",) if is_low_stock(r[5]) else ()
        tree.insert("", "end", values=r, tags=tags)

def search_by_sku(event=None):
    sku = sku_input.get().strip()
    if not sku:
        return
    product = get_product_by_sku(sku)
    if product:
        for i, label in enumerate(labels):
            entries[label].delete(0, tk.END)
            entries[label].insert(0, str(product[i+1]))
        global selected_id
        selected_id = product[0]
    else:
        messagebox.showwarning("Not Found", f"No product found with SKU '{sku}'")
    sku_input.delete(0, tk.END)

tk.Button(search_frame, text="Search", command=load_products).pack(side=tk.LEFT, padx=10)
sku_input.bind("<Return>", search_by_sku)

# --- Treeview ---
tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

columns = ["ID", "Name", "SKU", "Category", "Price", "Quantity", "Expiry Date"]
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.tag_configure("low", background=LOW_STOCK_COLOR)
tree.pack(fill="both", expand=True)

def on_tree_select(event):
    global selected_id
    item = tree.selection()
    if item:
        data = tree.item(item)['values']
        selected_id = data[0]
        for i, label in enumerate(labels):
            entries[label].delete(0, tk.END)
            entries[label].insert(0, str(data[i+1]))

tree.bind("<<TreeviewSelect>>", on_tree_select)

# --- Apply Theme & Load ---
apply_dark_theme(root)
load_products()

root.mainloop()
