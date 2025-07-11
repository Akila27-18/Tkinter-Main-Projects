import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from database import get_all_flashcards
from datetime import datetime

def show_stats():
    counts = {"Today": 0, "1d": 0, "3d": 0, "7d": 0, "Future": 0}
    today = datetime.now()

    for _, _, _, interval, due in get_all_flashcards():
        days_diff = (datetime.strptime(due, "%Y-%m-%d") - today).days
        if days_diff <= 0:
            counts["Today"] += 1
        elif days_diff <= 1:
            counts["1d"] += 1
        elif days_diff <= 3:
            counts["3d"] += 1
        elif days_diff <= 7:
            counts["7d"] += 1
        else:
            counts["Future"] += 1

    win = tk.Toplevel()
    win.title("Progress Statistics")

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(counts.keys(), counts.values(), color="skyblue")
    ax.set_title("Flashcard Review Progress")
    ax.set_ylabel("Number of Cards")

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack()
