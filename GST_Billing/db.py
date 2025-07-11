import sqlite3

def init_db():
    conn = sqlite3.connect("bills.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            contact TEXT,
            total REAL,
            gst_total REAL,
            grand_total REAL,
            bill_date TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS bill_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id INTEGER,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            gst_percent REAL NOT NULL,
            subtotal REAL,
            gst_amount REAL,
            total REAL,
            FOREIGN KEY(bill_id) REFERENCES bills(bill_id)
        )
    """)
    conn.commit()
    conn.close()
