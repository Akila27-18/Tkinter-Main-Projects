import sqlite3

def fetch_monthly_report(month, year, client_name):
    conn = sqlite3.connect("bills.db")
    c = conn.cursor()
    query = """
        SELECT * FROM bills 
        WHERE strftime('%m', bill_date)=? AND strftime('%Y', bill_date)=? AND client_name=?
    """
    c.execute(query, (month.zfill(2), year, client_name))
    results = c.fetchall()
    conn.close()
    return results
