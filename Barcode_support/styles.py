# styles.py

# Dark Theme Colors
DARK_BG = "#1e1e2f"
DARK_FG = "#ffffff"
ENTRY_BG = "#2e2e3e"
ENTRY_FG = "#ffffff"
BUTTON_BG = "#3e3e5c"
BUTTON_FG = "#ffffff"
HIGHLIGHT = "#4c8bf5"
LOW_STOCK_COLOR = "#ff4d4d"

FONT = ("Segoe UI", 10)

def apply_dark_theme(widget):
    """Recursively applies dark theme to all Tkinter widgets."""
    try:
        widget.configure(bg=DARK_BG, fg=DARK_FG)
    except:
        pass

    for child in widget.winfo_children():
        cls = child.__class__.__name__
        try:
            if cls in ['Label', 'Button']:
                child.configure(bg=DARK_BG, fg=DARK_FG, font=FONT)
            elif cls == 'Entry':
                child.configure(bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=DARK_FG, font=FONT)
            elif cls == 'Text':
                child.configure(bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=DARK_FG, font=FONT)
            elif cls in ['Frame', 'LabelFrame']:
                child.configure(bg=DARK_BG)
            elif cls == 'Checkbutton':
                child.configure(bg=DARK_BG, fg=DARK_FG, selectcolor=ENTRY_BG)
        except:
            pass
        apply_dark_theme(child)
