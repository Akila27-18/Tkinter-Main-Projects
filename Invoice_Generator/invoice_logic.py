# invoice_logic.py
from datetime import datetime
from database import get_next_invoice_no

TAX_RATE = 0.18  # 18% GST

def generate_invoice_number():
    return get_next_invoice_no()

def validate_invoice_fields(client, product, qty, price):
    errors = []
    if not client.strip():
        errors.append("Client name is required.")
    if not product.strip():
        errors.append("Product/Service is required.")
    try:
        qty = int(qty)
        if qty <= 0:
            errors.append("Quantity must be a positive integer.")
    except ValueError:
        errors.append("Quantity must be a number.")
    try:
        price = float(price)
        if price <= 0:
            errors.append("Unit Price must be a positive number.")
    except ValueError:
        errors.append("Unit Price must be a number.")

    return errors

def calculate_totals(qty, price):
    subtotal = qty * price
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return round(subtotal, 2), round(tax, 2), round(total, 2)

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
