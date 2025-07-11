import tkinter as tk
from markdown2 import markdown

class MarkdownPreview(tk.Text):
    def __init__(self, parent):
        super().__init__(parent, wrap='word', bg='#f4f4f4', state='disabled')
    
    def update_preview(self, content):
        html = markdown(content)
        self.config(state='normal')
        self.delete("1.0", tk.END)
        self.insert(tk.END, html)
        self.config(state='disabled')
