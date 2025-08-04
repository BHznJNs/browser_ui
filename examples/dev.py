import time
import _import_package as _
from browser_ui import BrowserUI, EventType

def test(data: dict):
    print(data)
    return data["a"] + data["b"]

def on_load():
    print("on_load")

def on_close():
    print("on_close")

ui = BrowserUI(dev_server_url="http://localhost:5173/")
ui.register("test", test)
ui.add_event_listener(EventType.page_loaded, on_load)
ui.add_event_listener(EventType.page_closed, on_close)
ui.start()

if __name__ == "__main__":
    try:
        while True: time.sleep(1) 
    except KeyboardInterrupt:
        ui.stop()
