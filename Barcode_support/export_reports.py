# export_reports.py
import csv
from tkinter import filedialog, messagebox
import sqlite3

DB_NAME = "inventory.db"

# --- EXPORT TO CSV ---
def export_inventory_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    headers = [desc[0] for desc in c.description]
    conn.close()

    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        messagebox.showinfo("Success", f"Inventory exported to CSV:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export CSV:\n{e}")

# --- EXPORT TO PDF ---
def export_inventory_pdf():
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                             filetypes=[("PDF Files", "*.pdf")])
    if not file_path:
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, sku, category, price, quantity, expiry_date FROM products ORDER BY name")
    rows = c.fetchall()
    conn.close()

    try:
        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 40, "Inventory Stock Report")

        c.setFont("Helvetica", 10)
        headers = ["Name", "SKU", "Category", "Price", "Qty", "Expiry"]
        x_offsets = [50, 150, 250, 350, 420, 470]
        y = height - 70

        for i, header in enumerate(headers):
            c.drawString(x_offsets[i], y, header)
        y -= 15
        c.line(50, y, 540, y)
        y -= 20

        for row in rows:
            if y < 60:
                c.showPage()
                y = height - 60
            for i, item in enumerate(row):
                c.drawString(x_offsets[i], y, str(item))
            y -= 18

        c.save()
        messagebox.showinfo("Success", f"Inventory exported to PDF:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export PDF:\n{e}")
