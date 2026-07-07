from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from .redshift import dashboard_payload
from .telemetry import measured


class RegionFlowHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/api/dashboard":
            self.send_response(404)
            self.end_headers()
            return

        body = json.dumps(measured("dashboard", dashboard_payload)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host: str = "0.0.0.0", port: int = 8080) -> None:
    HTTPServer((host, port), RegionFlowHandler).serve_forever()


if __name__ == "__main__":
    run()
