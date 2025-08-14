import time
import _import_package
from threading import Thread
from browser_ui import BrowserUI

def send_events(ui: BrowserUI):
    time.sleep(2)
    count = 0
    while True:
        ui.send_event("message", f"This is message number {count}")
        count += 1
        time.sleep(2)
        ui.send_event("greeting", f"Hello number {count}")
        time.sleep(2)

if __name__ == "__main__":
    ui = BrowserUI(static_dir="sse")
    
    event_thread = Thread(target=send_events, args=[ui], daemon=True)
    event_thread.start()

    ui.start()
    try:
        while True: time.sleep(1) 
    except KeyboardInterrupt:
        ui.stop()