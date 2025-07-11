from pynput import mouse, keyboard
import threading
import time

class IdleDetector:
    def __init__(self, idle_time=60, callback=None):
        self.idle_time = idle_time
        self.callback = callback
        self.last_activity = time.time()
        self.running = True
        self._start_listeners()
        threading.Thread(target=self._check_idle, daemon=True).start()

    def _on_activity(self, *args):
        self.last_activity = time.time()

    def _start_listeners(self):
        mouse.Listener(on_move=self._on_activity, on_click=self._on_activity, on_scroll=self._on_activity).start()
        keyboard.Listener(on_press=self._on_activity).start()

    def _check_idle(self):
        while self.running:
            if time.time() - self.last_activity > self.idle_time:
                if self.callback:
                    self.callback()
            time.sleep(5)

    def stop(self):
        self.running = False
