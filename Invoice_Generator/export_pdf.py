# export_pdf.py
from tkinter import filedialog, messagebox
from database import get_invoice_by_no
from datetime import datetime

# Toggle PDF export method: 'reportlab' or 'fpdf'
EXPORT_ENGINE = 'reportlab'  # change to 'fpdf' if preferred

# REPORTLAB
def export_with_reportlab(invoice_no, save_path=None):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    data = get_invoice_by_no(invoice_no)
    if not data:
        messagebox.showerror("Error", "Invoice not found.")
        return

    if not save_path:
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not save_path:
            return

    c = canvas.Canvas(save_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 800, f"Invoice #: {data[1]}")
    c.setFont("Helvetica", 12)
    c.drawString(100, 780, f"Date: {data[2]}")
    c.drawString(100, 760, f"Client: {data[3]}")
    c.line(50, 740, 550, 740)

    c.drawString(100, 720, f"Product/Service: {data[4]}")
    c.drawString(100, 700, f"Quantity: {data[5]}")
    c.drawString(100, 680, f"Unit Price: ₹{data[6]:.2f}")
    c.drawString(100, 660, f"Subtotal: ₹{data[7]:.2f}")
    c.drawString(100, 640, f"GST (18%): ₹{data[8]:.2f}")
    c.drawString(100, 620, f"Total: ₹{data[9]:.2f}")

    c.drawString(100, 580, "Thank you for your business!")
    c.save()

    messagebox.showinfo("Exported", f"Invoice saved as PDF:\n{save_path}")

# FPDF
def export_with_fpdf(invoice_no, save_path=None):
    from fpdf import FPDF

    data = get_invoice_by_no(invoice_no)
    if not data:
        messagebox.showerror("Error", "Invoice not found.")
        return

    if not save_path:
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not save_path:
            return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Invoice #: {data[1]}", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Date: {data[2]}", ln=True)
    pdf.cell(0, 10, f"Client: {data[3]}", ln=True)
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.cell(0, 10, f"Product/Service: {data[4]}", ln=True)
    pdf.cell(0, 10, f"Quantity: {data[5]}", ln=True)
    pdf.cell(0, 10, f"Unit Price: ₹{data[6]:.2f}", ln=True)
    pdf.cell(0, 10, f"Subtotal: ₹{data[7]:.2f}", ln=True)
    pdf.cell(0, 10, f"GST (18%): ₹{data[8]:.2f}", ln=True)
    pdf.cell(0, 10, f"Total: ₹{data[9]:.2f}", ln=True)

    pdf.ln(10)
    pdf.cell(0, 10, "Thank you for your business!", ln=True)
    pdf.output(save_path)

    messagebox.showinfo("Exported", f"Invoice saved as PDF:\n{save_path}")

# Controller function
def export_invoice_to_pdf(invoice_no, engine=EXPORT_ENGINE):
    if engine == "reportlab":
        export_with_reportlab(invoice_no)
    elif engine == "fpdf":
        export_with_fpdf(invoice_no)
    else:
        messagebox.showerror("Export Error", "Unknown PDF export engine.")
