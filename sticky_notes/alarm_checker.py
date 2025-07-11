import threading
import time
from datetime import datetime
from db import get_all_notes
import tkinter.messagebox as msgbox

def check_alarms(app):
    def run():
        shown_ids = set()
        while True:
            notes = get_all_notes()
            for note in notes:
                note_id, _, _, _, _, reminder = note
                if reminder and note_id not in shown_ids:
                    try:
                        rem_time = datetime.strptime(reminder, "%Y-%m-%d %H:%M")
                        if datetime.now() >= rem_time:
                            shown_ids.add(note_id)
                            app.after(0, lambda nid=note_id: msgbox.showinfo("Reminder", f"Reminder for note #{nid}!"))
                    except Exception:
                        pass
            time.sleep(30)
    threading.Thread(target=run, daemon=True).start()
