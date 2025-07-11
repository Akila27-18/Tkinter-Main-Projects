# styles.py

# Main dark theme colors
DARK_BG = "#1e1e2f"
DARK_FG = "#ffffff"
DARK_ENTRY_BG = "#2e2e3e"
DARK_ENTRY_FG = "#ffffff"
BUTTON_BG = "#3e3e5c"
BUTTON_FG = "#ffffff"
ACCENT = "#4c8bf5"

FONT = ("Segoe UI", 10)

def apply_dark_theme(widget):
    # Recursively apply dark theme to widget and children
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
                child.configure(bg=DARK_ENTRY_BG, fg=DARK_ENTRY_FG, insertbackground=DARK_FG, font=FONT)
            elif cls == 'Text':
                child.configure(bg=DARK_ENTRY_BG, fg=DARK_ENTRY_FG, insertbackground=DARK_FG, font=FONT)
            elif cls == 'Frame' or cls == 'LabelFrame':
                child.configure(bg=DARK_BG)
            elif cls == 'TCombobox':
                pass  # ttk widgets styled separately if needed
        except:
            pass
        apply_dark_theme(child)
