import json
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

BASE_DIR = os.path.expanduser("~/agente_xauusd")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
SINAIS_PATH = os.path.join(BASE_DIR, "dados", "sinais.csv")

def carregar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def carregar_sinais(max_rows=50):
    if not os.path.exists(SINAIS_PATH):
        return []
    sinais = []
    with open(SINAIS_PATH, "r", encoding="utf-8") as f:
        headers = f.readline().strip().split(",")
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != len(headers):
                continue
            sinais.append(dict(zip(headers, parts)))
    sinais.reverse()
    return sinais[:max_rows]

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/config":
            try:
                cfg = carregar_config()
                self._set_headers()
                self.wfile.write(json.dumps(cfg).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        elif parsed.path == "/sinais":
            try:
                sinais = carregar_sinais()
                self._set_headers()
                self.wfile.write(json.dumps(sinais).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "not found"}).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/config":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode("utf-8"))
                cfg = carregar_config()
                cfg.update(data)
                salvar_config(cfg)
                self._set_headers()
                self.wfile.write(json.dumps({"status": "ok", "config": cfg}).encode("utf-8"))
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "not found"}).encode("utf-8"))

def run_server(port=8000):
    os.chdir(BASE_DIR)
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Servidor HTTP rodando em http://127.0.0.1:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
