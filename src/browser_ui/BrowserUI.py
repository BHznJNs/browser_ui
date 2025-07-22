import queue
import webbrowser
import importlib.resources as pkg_resources
from typing import Callable
from pathlib import Path
from threading import Thread, Event
from cheroot import wsgi
from bottle import Bottle, abort, request, static_file, response

from browser_ui.utils import SerializableCallable, EventType
from .utils import get_caller_file_abs_path

INJECTED_SCRIPT_PATH = pkg_resources.files("browser_ui").joinpath("injected_script.js")
with open(str(INJECTED_SCRIPT_PATH), "r") as f:
    INJECTED_SCRIPT = f.read()

def server_factory(app: Bottle, port: int, server_name: str='browser-ui-server') -> wsgi.Server:
    return wsgi.Server(
        ('localhost', port), app,
        server_name=server_name,
    )

class BrowserUI:
    def __init__(self, static_dir: str, port: int = 8080):
        self._is_used = False
        self._port = port
        self._stop_event = Event()
        self._static_dir = Path(get_caller_file_abs_path()).parent.joinpath(static_dir)
        self._thread = Thread(target=self._run)

        self._app = Bottle()
        self._method_map: dict[str, SerializableCallable] = {}
        self._event_map: dict[EventType, list[SerializableCallable]] = {}
        self._server = server_factory(self._app, port)
        self._sse_queue = queue.Queue()
        self._app.route("/", callback=self._serve_static_file)
        self._app.route("/<path:path>", callback=self._serve_static_file)
        self._app.route("/__method__/<method_name>", method="POST", callback=self._serve_method)
        self._app.route("/__event__/<event_name>", method="POST", callback=self._serve_event)
        self._app.route("/__sse__", callback=self._serve_sse)

    def _run(self):
        try:
            self._server.prepare()
            self._server.serve()
        except Exception as e:
            print(f"Server error: {e}")

    def _serve_html_file(self, path: str) -> str:
        with open(str(Path(self._static_dir).joinpath(path)), "r") as f:
            html_content = f.read()
        return html_content.replace("<body>", f"""<body><script>{INJECTED_SCRIPT}</script>""")

    def _serve_static_file(self, path: str="index.html"):
        if path.endswith(".html") or path.endswith(".htm"):
            return self._serve_html_file(path)
        return static_file(path, root=self._static_dir)

    def _serve_method(self, method_name: str):
        data = request.json
        if method_name not in self._method_map:
            abort(404, f"Method {method_name} is not implemented.")
        res = self._method_map[method_name](data)
        return res
    
    def _serve_event(self, event_name: str):
        event = EventType.from_str(event_name)
        if event not in self._event_map:
            abort(404, f"Event {event_name} is not implemented.")
        for callback in self._event_map[event]:
            callback()

    def _serve_sse(self):
        response.set_header("Content-Type", "text/event-stream")
        response.set_header("Cache-Control", "no-cache")
        while not self._stop_event.is_set():
            try:
                event, data = self._sse_queue.get(timeout=0.01)
                yield f"event: {event}\ndata: {data}\n\n"
            except queue.Empty: continue

    def add_event_listener(self, event_type: EventType, callback: Callable):
        if event_type not in self._event_map:
            self._event_map[event_type] = []
        self._event_map[event_type].append(callback)

    def register(self, method_name: str, method: SerializableCallable):
        self._method_map[method_name] = method

    def send_event(self, event: str, data: str):
        self._sse_queue.put((event, data))

    def start(self):
        if self._is_used:
            raise RuntimeError("This BrowserUI instance has already been used and cannot be reused.")
        self._thread.start()
        webbrowser.open_new_tab(f"http://localhost:{self._port}")

    def stop(self):
        self._stop_event.set()
        self._server.stop()
        self._thread.join()
        self._is_used = True
