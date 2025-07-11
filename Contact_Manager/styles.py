
def apply_dark_theme(widget):
    try:
        widget.configure(bg="#1e1e2f", fg="white")
    except:
        pass
    for child in widget.winfo_children():
        try:
            child.configure(bg="#1e1e2f", fg="white", insertbackground="white")
        except:
            pass
        apply_dark_theme(child)
