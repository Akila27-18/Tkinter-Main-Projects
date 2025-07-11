def make_draggable(widget, on_drop_callback):
    widget.bind("<ButtonPress-1>", lambda e: widget.start_drag(e))
    widget.bind("<B1-Motion>", lambda e: widget.drag(e))
    widget.bind("<ButtonRelease-1>", lambda e: on_drop_callback())
