import time
import _import_package as _
from browser_ui import BrowserUI, EventType

def on_load():
    print("on_load")

def on_close():
    print("on_close")

ui = BrowserUI("./events/")
ui.add_event_listener(EventType.page_loaded, on_load)
ui.add_event_listener(EventType.page_closed, on_close)
ui.start()

if __name__ == "__main__":
    try:
        while True: time.sleep(1) 
    except KeyboardInterrupt:
        ui.stop()
