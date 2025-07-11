# export_utils.py
import csv
from fpdf import FPDF
import sqlite3

def export_to_csv():
    conn = sqlite3.connect("results.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()
    with open("exports/result_export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll", "Name", "Sub1", "Sub2", "Sub3", "Total", "Average"])
        writer.writerows(data)


def export_to_pdf():
    conn = sqlite3.connect("results.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Student Results", ln=True, align="C")
    pdf.set_font("Arial", "", 10)

    for row in data:
        line = f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]}"
        pdf.cell(190, 8, line, ln=True)

    pdf.output("exports/result_export.pdf")
