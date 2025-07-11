import tkinter as tk
from tkinter import ttk
import database
from tkinter import messagebox

class ReviewUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Review Flashcards")
        self.flashcards = database.get_due_flashcards()
        self.index = 0
        self.flipped = False
        self.setup_ui()
        self.load_card()

    def setup_ui(self):
        self.card_label = ttk.Label(self.root, text="", wraplength=300, font=("Helvetica", 16))
        self.card_label.pack(padx=20, pady=20)
        self.card_label.bind("<Button-1>", self.flip_card)

        frame = ttk.Frame(self.root)
        frame.pack()

        for difficulty in ["Easy", "Medium", "Hard"]:
            ttk.Button(frame, text=difficulty, command=lambda d=difficulty: self.mark_card(d)).pack(side="left", padx=5)

    def load_card(self):
        if self.index >= len(self.flashcards):
            self.card_label.config(text="All done for today!")
            return
        self.flipped = False
        self.current = self.flashcards[self.index]
        self.card_label.config(text=self.current[1])

    def flip_card(self, e):
        self.flipped = not self.flipped
        self.card_label.config(text=self.current[2] if self.flipped else self.current[1])

    def mark_card(self, difficulty):
        database.update_review(self.current[0], difficulty)
        self.index += 1
        self.load_card()
    def load_next_card(self):
        card = database.get_next_card()
        if card:
            card_id, question, answer = card
            self.current = card  # ← THIS SETS self.current CORRECTLY
            self.question_label.config(text=question)
            ...
        else:
            messagebox.showinfo("Done", "No more cards to review.")
            self.current = None

