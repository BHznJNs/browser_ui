import time
import _import_package as _
from browser_ui import BrowserUI

def test(data: dict):
    print(data)
    return data["a"] + data["b"]

ui = BrowserUI("./binding/")
ui.register_method("test", test)
ui.start()

if __name__ == "__main__":
    try:
        while True: time.sleep(1) 
    except KeyboardInterrupt:
        ui.stop()
