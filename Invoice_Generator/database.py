# database.py
import sqlite3

DB_NAME = "invoices.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_no TEXT,
        date TEXT,
        client_name TEXT,
        product TEXT,
        quantity INTEGER,
        unit_price REAL,
        subtotal REAL,
        tax REAL,
        total REAL
    )''')
    conn.commit()
    conn.close()

def insert_invoice(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT INTO invoices (invoice_no, date, client_name, product, quantity,
                 unit_price, subtotal, tax, total)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()

def get_filtered_invoices(client_filter="", date_filter=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    query = "SELECT invoice_no, date, client_name, total FROM invoices"
    filters = []
    params = []

    if client_filter:
        filters.append("client_name LIKE ?")
        params.append(f"%{client_filter}%")
    if date_filter:
        filters.append("date LIKE ?")
        params.append(f"{date_filter}%")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    c.execute(query, params)
    results = c.fetchall()
    conn.close()
    return results

def get_invoice_by_no(invoice_no):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM invoices WHERE invoice_no=?", (invoice_no,))
    result = c.fetchone()
    conn.close()
    return result

def get_next_invoice_no():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT MAX(id) FROM invoices")
    max_id = c.fetchone()[0]
    conn.close()
    return f"INV-{(max_id or 0) + 1:05d}"
