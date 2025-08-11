import time
import _import_package
from typing import Generator
from browser_ui import BrowserUI

def fibonacci(limit: int) -> Generator[int, None, None]:
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1
        time.sleep(1)

if __name__ == "__main__":
    ui = BrowserUI(static_dir="./generator/")
    ui.register_method("fibonacci", fibonacci)
    ui.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ui.stop()
