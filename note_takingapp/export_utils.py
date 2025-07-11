from tkinter import filedialog
from reportlab.pdfgen import canvas

def export_to_txt(title, content):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=title)
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def export_to_pdf(title, content):
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=title)
    if file_path:
        pdf = canvas.Canvas(file_path)
        text_obj = pdf.beginText(40, 800)
        for line in content.split('\n'):
            text_obj.textLine(line)
        pdf.drawText(text_obj)
        pdf.save()
