#!/usr/bin/env python3
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE_DIR = os.path.expanduser("~/agente_xauusd")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def carregar_config():
    default = {"lote": 0.01, "intervalo_min": 15}
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except:
        return default

print("🚀 Servidor iniciando...")
print(f"📁 Pasta: {BASE_DIR}")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            config = carregar_config()
            self.wfile.write(json.dumps(config).encode())
        else:
            self.send_response(404)
            self.end_headers()

print("✅ Servidor rodando: http://127.0.0.1:8000")
httpd = HTTPServer(('127.0.0.1', 8000), Handler)
httpd.serve_forever()
