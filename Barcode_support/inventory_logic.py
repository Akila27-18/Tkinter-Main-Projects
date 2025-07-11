# inventory_logic.py

LOW_STOCK_THRESHOLD = 5  # Trigger red alert if quantity ≤ this

def validate_product_fields(name, sku, category, price, quantity, expiry_date):
    errors = []
    if not name.strip():
        errors.append("Product name is required.")
    if not sku.strip():
        errors.append("SKU is required.")
    if not category.strip():
        errors.append("Category is required.")

    try:
        price = float(price)
        if price <= 0:
            errors.append("Price must be greater than 0.")
    except ValueError:
        errors.append("Price must be a valid number.")

    try:
        quantity = int(quantity)
        if quantity < 0:
            errors.append("Quantity cannot be negative.")
    except ValueError:
        errors.append("Quantity must be an integer.")

    # Optional: validate expiry date format (YYYY-MM-DD)
    if expiry_date.strip():
        if not validate_date_format(expiry_date):
            errors.append("Expiry date must be in YYYY-MM-DD format.")

    return errors

def validate_date_format(date_str):
    from datetime import datetime
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_low_stock(quantity):
    return int(quantity) <= LOW_STOCK_THRESHOLD
