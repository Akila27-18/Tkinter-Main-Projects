from database import get_connection
from datetime import datetime

def issue_book(book_id, student_name):
    conn = get_connection()
    c = conn.cursor()

    issue_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO issues (book_id, student_name, issue_date) VALUES (?, ?, ?)", (book_id, student_name, issue_date))
    c.execute("UPDATE books SET is_issued = 1 WHERE id = ?", (book_id,))
    
    conn.commit()
    conn.close()
