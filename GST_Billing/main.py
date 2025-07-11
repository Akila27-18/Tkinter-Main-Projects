import tkinter as tk
from ui.billing_form import launch_billing_form
from ui.report_viewer import launch_report_viewer

def launch_dashboard():
    root = tk.Tk()
    root.title("Billing System Dashboard")

    tk.Label(root, text="Welcome to Billing System", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="🧾 New Bill Entry", font=("Arial", 12), width=25, command=launch_billing_form).pack(pady=10)
    tk.Button(root, text="📊 Monthly Report Viewer", font=("Arial", 12), width=25, command=launch_report_viewer).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    launch_dashboard()
