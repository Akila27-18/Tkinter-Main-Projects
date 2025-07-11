from datetime import datetime

def is_overdue(due_date_str):
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        return due_date < datetime.now()
    except:
        return False
