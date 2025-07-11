from fpdf import FPDF

def export_bill_to_pdf(bill_data, items, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Billing Invoice", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Client: {bill_data['client_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {bill_data['bill_date']}", ln=True)
    pdf.ln(10)
    for item in items:
        pdf.cell(200, 10, txt=f"{item['item_name']} - Qty: {item['quantity']}, Price: {item['price']}, GST: {item['gst_percent']}%", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Grand Total: ₹{bill_data['grand_total']}", ln=True)
    pdf.output(filename)
