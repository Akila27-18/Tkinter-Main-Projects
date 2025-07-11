import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from bill_generator import calculate_totals
from db import init_db
import sqlite3

def launch_billing_form():
    init_db()
    items = []

    def add_item():
        name = entry_item.get()
        try:
            qty = int(entry_qty.get())
            price = float(entry_price.get())
            gst = float(entry_gst.get())
            if name and qty > 0 and price > 0:
                items.append({'item_name': name, 'quantity': qty, 'price': price, 'gst_percent': gst})
                messagebox.showinfo("Added", f"{name} added!")
            else:
                raise ValueError
        except:
            messagebox.showerror("Invalid", "Enter valid details")

    def save_bill():
        client = entry_client.get()
        contact = entry_contact.get()
        if not client:
            messagebox.showerror("Missing", "Client name is required")
            return
        if not items:
            messagebox.showerror("Missing", "Add at least one item")
            return
        calculate_totals(items)
        total = sum(i['subtotal'] for i in items)
        gst_total = sum(i['gst_amount'] for i in items)
        grand_total = total + gst_total
        date = datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect("bills.db")
        c = conn.cursor()
        c.execute("INSERT INTO bills (client_name, contact, total, gst_total, grand_total, bill_date) VALUES (?, ?, ?, ?, ?, ?)", (client, contact, total, gst_total, grand_total, date))
        bill_id = c.lastrowid
        for i in items:
            c.execute("INSERT INTO bill_items (bill_id, item_name, quantity, price, gst_percent, subtotal, gst_amount, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (bill_id, i['item_name'], i['quantity'], i['price'], i['gst_percent'], i['subtotal'], i['gst_amount'], i['total']))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", f"Bill saved with ID {bill_id}")
        root.destroy()

    root = tk.Tk()
    root.title("Billing System with GST")

    tk.Label(root, text="Client Name").grid(row=0, column=0)
    entry_client = tk.Entry(root)
    entry_client.grid(row=0, column=1)
    tk.Label(root, text="Contact").grid(row=1, column=0)
    entry_contact = tk.Entry(root)
    entry_contact.grid(row=1, column=1)

    tk.Label(root, text="Item").grid(row=2, column=0)
    entry_item = tk.Entry(root)
    entry_item.grid(row=2, column=1)
    tk.Label(root, text="Qty").grid(row=3, column=0)
    entry_qty = tk.Entry(root)
    entry_qty.grid(row=3, column=1)
    tk.Label(root, text="Price").grid(row=4, column=0)
    entry_price = tk.Entry(root)
    entry_price.grid(row=4, column=1)
    tk.Label(root, text="GST %").grid(row=5, column=0)
    entry_gst = tk.Entry(root)
    entry_gst.grid(row=5, column=1)

    tk.Button(root, text="Add Item", command=add_item).grid(row=6, column=1)
    tk.Button(root, text="Save Bill", command=save_bill).grid(row=7, column=1)
    root.mainloop()
