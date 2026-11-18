from __future__ import annotations
import hmac, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .config import load_config
from .tools import call_tool, catalog

def serve():
    cfg = load_config()
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, obj):
            raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        def _auth(self):
            header = self.headers.get("Authorization", "")
            token = header[7:] if header.startswith("Bearer ") else ""
            return hmac.compare_digest(token, cfg["token"])
        def do_GET(self):
            if not self._auth(): return self._send(401, {"ok": False, "error": {"code": "UNAUTHORIZED"}})
            if self.path == "/health": return self._send(200, {"ok": True, "name": "phone-agent-cli", "version": "0.1.0"})
            if self.path == "/v1/tools": return self._send(200, {"ok": True, "data": {"tools": catalog()}})
            self._send(404, {"ok": False, "error": {"code": "NOT_FOUND"}})
        def do_POST(self):
            if not self._auth(): return self._send(401, {"ok": False, "error": {"code": "UNAUTHORIZED"}})
            if self.path != "/v1/call": return self._send(404, {"ok": False, "error": {"code": "NOT_FOUND"}})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 256_000: return self._send(413, {"ok": False, "error": {"code": "BODY_SIZE"}})
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict): raise ValueError("JSON body must be an object")
                result = call_tool(body["tool"], body.get("arguments", {}), cfg)
                self._send(200, {"ok": True, "tool": body["tool"], "data": result})
            except Exception as e:
                self._send(400, {"ok": False, "error": {"code": type(e).__name__.upper(), "message": str(e)}})
        def log_message(self, *_): pass
    host, port = cfg["host"], int(cfg["port"])
    if host not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("Refusing non-loopback bind in MVP; use a secured tunnel for remote access")
    print(f"Phone Agent API listening on http://{host}:{port}")
    print("Keep this Termux session open. Press Ctrl+C to stop.")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
