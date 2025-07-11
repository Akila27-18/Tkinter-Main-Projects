
import threading
import time
from tkinter import messagebox
from datetime import datetime

reminders = []

def schedule_reminder(task, root):
    def reminder_thread():
        now = datetime.now()
        due = datetime.strptime(task['datetime'], "%Y-%m-%d %H:%M")
        delay = (due - now).total_seconds()
        if delay > 0:
            time.sleep(delay)
        root.after(0, lambda: messagebox.showinfo("Reminder", f"Task Due: {task['title']}\n{task['description']}"))

    t = threading.Thread(target=reminder_thread, daemon=True)
    t.start()
    reminders.append(t)
