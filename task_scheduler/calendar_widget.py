
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk

def create_datetime_picker(parent):
    date_entry = DateEntry(parent, width=12, background='darkblue',
                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    hour_box = ttk.Combobox(parent, values=[f"{h:02d}" for h in range(24)], width=3)
    hour_box.set("09")
    min_box = ttk.Combobox(parent, values=[f"{m:02d}" for m in range(0, 60, 5)], width=3)
    min_box.set("00")
    return date_entry, hour_box, min_box
