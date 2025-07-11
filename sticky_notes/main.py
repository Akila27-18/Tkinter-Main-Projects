import tkinter as tk
from tkinter import colorchooser, simpledialog
from db import init_db, get_all_notes, save_note, delete_note
from alarm_checker import check_alarms
from datetime import datetime

class StickyNote(tk.Toplevel):
    def __init__(self, master, note_id=None, content="", x=100, y=100, color="#ffff88", reminder=""):
        super().__init__(master)
        self.master = master
        self.note_id = note_id
        self.geometry(f"200x200+{x}+{y}")
        self.configure(bg=color)
        self.color = color
        self.reminder = reminder

        self.text = tk.Text(self, bg=color, wrap="word")
        self.text.insert("1.0", content)
        self.text.pack(expand=True, fill="both")

        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)

        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Change Color", command=self.change_color)
        self.menu.add_command(label="Set Reminder", command=self.set_reminder)
        self.menu.add_command(label="Delete Note", command=self.delete_self)
        self.bind("<Button-3>", self.show_menu)

        self.protocol("WM_DELETE_WINDOW", self.save_and_close)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        dx = event.x - self._x
        dy = event.y - self._y
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.geometry(f"+{x}+{y}")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def change_color(self):
        color = colorchooser.askcolor(title="Pick Note Color")[1]
        if color:
            self.color = color
            self.text.config(bg=color)
            self.configure(bg=color)

    def set_reminder(self):
        reminder = simpledialog.askstring("Set Reminder", "Enter reminder (YYYY-MM-DD HH:MM):")
        try:
            if reminder:
                datetime.strptime(reminder, "%Y-%m-%d %H:%M")
                self.reminder = reminder
        except ValueError:
            tk.messagebox.showerror("Invalid Format", "Enter time in format YYYY-MM-DD HH:MM")

    def save_and_close(self):
        content = self.text.get("1.0", "end-1c")
        x = self.winfo_x()
        y = self.winfo_y()
        self.note_id = save_note(content, x, y, self.color, self.reminder, self.note_id)
        self.destroy()

    def delete_self(self):
        if self.note_id:
            delete_note(self.note_id)
        self.destroy()


class StickyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sticky Notes")
        self.geometry("300x100")
        tk.Button(self, text="New Note", command=self.create_note).pack(pady=20)

        self.load_notes()
        check_alarms(self)

    def create_note(self):
        StickyNote(self)

    def load_notes(self):
        notes = get_all_notes()
        for note in notes:
            note_id, content, x, y, color, reminder = note
            StickyNote(self, note_id, content, x, y, color, reminder)


if __name__ == "__main__":
    init_db()
    app = StickyApp()
    app.mainloop()
