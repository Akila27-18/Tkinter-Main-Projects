
import re

def validate_contact(name, phone, email):
    errors = []
    if not name.strip():
        errors.append("Name is required.")
    if not phone.strip().isdigit() or len(phone) < 7:
        errors.append("Phone must be numeric and at least 7 digits.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
        errors.append("Invalid email address.")
    return errors
