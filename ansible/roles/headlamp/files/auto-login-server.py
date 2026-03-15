#!/usr/bin/env python3
"""Serves a single HTML page that sets Headlamp cluster token then redirects to /."""
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.environ.get("HEADLAMP_TOKEN", "")
TOKEN_FILE = os.environ.get(
    "HEADLAMP_TOKEN_FILE", "/var/run/secrets/kubernetes.io/serviceaccount/token"
)
CLUSTER = os.environ.get("HEADLAMP_CLUSTER", "main")
TOKEN_SET_COOKIE_VALUE = os.environ.get("HEADLAMP_TOKEN_SET_COOKIE_VALUE", "v2")
# Base path for Headlamp UI (empty = /)
APP_PATH = os.environ.get("HEADLAMP_APP_PATH", "")
if not APP_PATH:
    APP_PATH = "/"


def _load_token():
    if TOKEN:
        return TOKEN
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


def html():
    # Escape for use inside a JS string
    tok = (_load_token() or "").replace("\\", "\\\\").replace("</script>", "<\\/script>").replace("'", "\\'")
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Headlamp</title></head><body>"
        "<p>Logging in...</p><script>"
        "var t='" + tok + "';"
        "if(!t){document.body.innerHTML='<p>No token.</p>';}else{"
        "fetch('" + (APP_PATH.rstrip("/") or "") + "/clusters/" + CLUSTER + "/set-token',{"
        "method:'POST',headers:{'Content-Type':'application/json'},"
        "body:JSON.stringify({token:t}),credentials:'include'"
        "}).then(function(){location.href='" + APP_PATH + "';})"
        ".catch(function(e){document.body.innerHTML='<p>Error: '+e+'</p>';});"
        "}</script></body></html>"
    ).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "":
            body = html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            # So Caddy can avoid redirecting / -> /internal-login again (prevents loop)
            self.send_header(
                "Set-Cookie",
                f"headlamp_token_set={TOKEN_SET_COOKIE_VALUE}; Path=/; Max-Age=86400; HttpOnly; Secure; SameSite=Lax",
            )
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    HTTPServer(("", port), Handler).serve_forever()
