"""Local preview server for the site, with caching off so every edit shows on reload.

    python tools/serve.py          # http://127.0.0.1:5600
    python tools/serve.py 8080     # any other port
"""
import http.server
import os
import sys


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        # Mirror GitHub Pages: unknown paths get the site's 404 page.
        if code == 404 and os.path.exists("404.html"):
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open("404.html", "rb") as f:
                self.wfile.write(f.read())
            return
        super().send_error(code, message, explain)


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5600
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), NoCacheHandler)
    print(f"Serving the site at http://127.0.0.1:{port}")
    server.serve_forever()
