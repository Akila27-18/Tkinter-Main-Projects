from datetime import datetime

def calculate_fine(issue_date_str, return_date_str, daily_rate=2):
    issue_date = datetime.strptime(issue_date_str, "%Y-%m-%d")
    return_date = datetime.strptime(return_date_str, "%Y-%m-%d")
    days = (return_date - issue_date).days
    overdue_days = max(0, days - 7)
    return overdue_days * daily_rate
