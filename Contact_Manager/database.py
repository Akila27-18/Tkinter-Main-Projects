
import sqlite3

DB_NAME = "contacts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT,
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_contact(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO contacts (name, phone, email, address, notes) VALUES (?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()

def update_contact(contact_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE contacts SET name=?, phone=?, email=?, address=?, notes=? WHERE id=?", (*data, contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()

def search_contacts(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    query = f"%{query}%"
    c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?", (query, query, query))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_contacts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM contacts")
    rows = c.fetchall()
    conn.close()
    return rows
