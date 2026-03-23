# Terminal 1: python3 coletor.py
import requests
import json
import time
import os
from datetime import datetime
def carregar_segredos():
    with open("config_secrets.json", "r") as f:
        return json.load(f)

segredos = carregar_segredos()
TOKEN = segredos["TELEGRAM_TOKEN"]
CHAT_ID = segredos["CHAT_ID"]
DB_FILE = "dados_xauusd.json"

def buscar_preco():
    try:
        r = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F?interval=1m&range=1d")
        data = r.json()
        preco = data['chart']['result'][0]['meta']['regularMarketPrice']
        return round(preco, 2)
    except:
        return None

def salvar_preco(preco):
    historico = []
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            historico = json.load(f)
    
    historico.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "preco": preco
    })
    
    # Manter só últimas 200 entradas
    historico = historico[-200:]
    
    with open(DB_FILE, 'w') as f:
        json.dump(historico, f)

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})

print("✅ Coletor iniciado — atualizando a cada 1 minuto...")
preco_anterior = None

while True:
    preco = buscar_preco()
    if preco:
        salvar_preco(preco)
        variacao = ""
        if preco_anterior:
            diff = round(preco - preco_anterior, 2)
            variacao = f"({'▲' if diff > 0 else '▼'} {abs(diff)})"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] XAUUSD: ${preco} {variacao}")
        preco_anterior = preco
    time.sleep(60)
