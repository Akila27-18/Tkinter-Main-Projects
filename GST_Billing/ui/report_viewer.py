import tkinter as tk
from tkinter import ttk, messagebox
from report_generator import fetch_monthly_report

def launch_report_viewer():
    def fetch_and_display():
        month = combo_month.get().strip()
        year = combo_year.get().strip()
        client = entry_client.get().strip()

        # Field Validations
        if not month or not year or not client:
            messagebox.showerror("Missing Information", "All fields are required.")
            return

        if not (month.isdigit() and 1 <= int(month) <= 12):
            messagebox.showerror("Invalid Month", "Month must be a number between 01 and 12.")
            return

        if not (year.isdigit() and 2000 <= int(year) <= 2100):
            messagebox.showerror("Invalid Year", "Year must be a 4-digit number between 2000 and 2100.")
            return

        if len(client) < 2:
            messagebox.showerror("Invalid Client Name", "Client name must be at least 2 characters long.")
            return

        # Fetch Data
        results = fetch_monthly_report(month.zfill(2), year, client)
        tree.delete(*tree.get_children())

        if not results:
            messagebox.showinfo("No Records", f"No bills found for {client} in {month}/{year}.")
        else:
            for row in results:
                tree.insert("", "end", values=row)

    # GUI Setup
    root = tk.Tk()
    root.title("Monthly Report Viewer")

    # Month
    tk.Label(root, text="Month (MM):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    combo_month = ttk.Combobox(root, values=[f"{i:02}" for i in range(1, 13)], width=10, state="readonly")
    combo_month.grid(row=0, column=1)

    # Year
    tk.Label(root, text="Year (YYYY):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    combo_year = ttk.Combobox(root, values=[str(y) for y in range(2020, 2031)], width=10, state="readonly")
    combo_year.grid(row=1, column=1)

    # Client Name
    tk.Label(root, text="Client Name:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_client = tk.Entry(root, width=30)
    entry_client.grid(row=2, column=1)

    # Search Button
    tk.Button(root, text="Search Report", command=fetch_and_display).grid(row=3, column=1, pady=10)

    # Treeview to Display Report
    tree = ttk.Treeview(root, columns=("ID", "Client", "Contact", "Total", "GST", "Grand Total", "Date"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()
