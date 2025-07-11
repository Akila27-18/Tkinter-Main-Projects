# database.py
import sqlite3

DB_NAME = "inventory.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- CREATE ---
def add_product(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO products (name, sku, category, price, quantity, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

# --- READ ---
def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products ORDER BY name ASC")
    rows = c.fetchall()
    conn.close()
    return rows

def search_products(name_filter="", category_filter=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    if name_filter:
        query += " AND name LIKE ?"
        params.append(f"%{name_filter}%")
    if category_filter:
        query += " AND category LIKE ?"
        params.append(f"%{category_filter}%")
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

# --- UPDATE ---
def update_product(product_id, data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE products
        SET name=?, sku=?, category=?, price=?, quantity=?, expiry_date=?
        WHERE id=?
    """, (*data, product_id))
    conn.commit()
    conn.close()

# --- DELETE ---
def delete_product(product_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()

# --- FETCH ONE ---
def get_product_by_sku(sku):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE sku=?", (sku,))
    row = c.fetchone()
    conn.close()
    return row
