import importlib.resources as pkg_resources
import webbrowser
from pathlib import Path
from threading import Thread
from cheroot import wsgi
from bottle import Bottle, static_file
from .utils import get_caller_file_abs_path

INJECTED_SCRIPT_PATH = pkg_resources.files('browser_ui').joinpath("injected_script.js")
with open(str(INJECTED_SCRIPT_PATH), "r") as f:
    INJECTED_SCRIPT = f.read()

def server_factory(app: Bottle, port: int, server_name: str='browser-ui-server') -> wsgi.Server:
    return wsgi.Server(
        ('localhost', port), app,
        server_name=server_name,
    )

class BrowserUI:
    def __init__(self,
                 static_dir: str,
                 port: int = 8080,
                 ):
        self._is_used = False
        self._port = port
        self._static_dir = Path(get_caller_file_abs_path()).parent.joinpath(static_dir)
        self._thread = Thread(target=self._run)

        app = self._app = Bottle()
        self._server = server_factory(app, port)
        app.route("/", callback=self._serve_index_page)
        app.route("/<path:path>", callback=self._serve_static_file)

    def _run(self):
        try:
            self._server.prepare()
            self._server.serve()
        except Exception as e:
            print(f"Server error: {e}")

    def _serve_index_page(self):
        index_path = Path(self._static_dir).joinpath("index.html")
        with open(str(index_path), "r") as f:
            index_content = f.read()
        return index_content.replace("<body>", f"""<body><script>{INJECTED_SCRIPT}</script>""")

    def _serve_static_file(self, path: str):
        return static_file(path, root=self._static_dir)

    def start(self):
        if self._is_used:
            raise RuntimeError("This BrowserUI instance has already been used and cannot be reused.")
        self._thread.start()
        webbrowser.open_new_tab(f"http://localhost:{self._port}")

    def stop(self):
        self._server.stop()
        self._thread.join()
        self._is_used = True
