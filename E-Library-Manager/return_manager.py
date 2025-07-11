from database import get_connection
from utils import calculate_fine
from datetime import datetime

def return_book(book_id):
    conn = get_connection()
    c = conn.cursor()

    return_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT id, issue_date FROM issues WHERE book_id = ? AND return_date IS NULL", (book_id,))
    row = c.fetchone()
    if row:
        issue_id, issue_date = row
        fine = calculate_fine(issue_date, return_date)
        c.execute("UPDATE issues SET return_date = ?, fine = ? WHERE id = ?", (return_date, fine, issue_id))
        c.execute("UPDATE books SET is_issued = 0 WHERE id = ?", (book_id,))
        conn.commit()
    conn.close()
