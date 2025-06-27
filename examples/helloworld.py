import time
import _import_package as _
from browser_ui import BrowserUI

ui = BrowserUI("./helloworld/")
ui.start()

if __name__ == "__main__":
    try:
        while True: time.sleep(1) 
    except KeyboardInterrupt:
        ui.stop()
