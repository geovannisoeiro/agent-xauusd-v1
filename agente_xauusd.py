import yfinance as yf
import requests
import time
import json
import os
from datetime import datetime

BASE_DIR = os.path.expanduser("~/agente_xauusd")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
SINAIS_PATH = os.path.join(BASE_DIR, "dados", "sinais.csv")

def carregar_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except:
        return {"telegram_token": "8656452017:AAH--Hf5dcNrhJytjSNtwdcokZpOPWxlFEw", "telegram_chat_id": "1029082401", "intervalo_min": 5}

def enviar_telegram(token, chat_id, msg):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    res = requests.post(url, data={"chat_id": chat_id, "text": msg})
    return res.status_code == 200

def salvar_sinal(sinal_texto):
    os.makedirs(os.path.dirname(SINAIS_PATH), exist_ok=True)
    com_cabecalho = not os.path.exists(SINAIS_PATH)
    
    with open(SINAIS_PATH, 'a') as f:
        if com_cabecalho:
            f.write("timestamp,sinal\n")
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{sinal_texto}\n")

print("🤖 Agente XAU/USD V1 COMPLETO Iniciado!")
cfg = carregar_config()
enviar_telegram(cfg['telegram_token'], cfg['telegram_chat_id'], "🚀 V1 Sistema Completo Online: Painel + Dados Reais + Telegram")

while True:
    try:
        cfg = carregar_config() # Lê painel em tempo real
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Verificando XAUUSD (dados reais)...")
        
        # Pega Ouro Real
        df = yf.download("GC=F", period="1d", interval="1m", progress=False)
        preco_atual = float(df['Close'].iloc[-1].item())
        preco_ant = float(df['Close'].iloc[-2].item())
        diff = preco_atual - preco_ant
        
        print(f"  💰 Preço: ${preco_atual:.2f} | 📉 Ant: ${preco_ant:.2f}")
        
        # Lógica de sinal simplificada (se moveu mais que $0.10)
        sinal = None
        if diff > 0.10:
            sinal = "🟢 COMPRA"
        elif diff < -0.10:
            sinal = "🔴 VENDA"
            
        if sinal:
            print(f"  🎯 {sinal} DETECTADO!")
            msg = f"🚨 SINAL XAU/USD\n\n{sinal}\n💰 Preço: ${preco_atual:.2f}\n📊 Variação: ${diff:.2f}"
            enviar_telegram(cfg['telegram_token'], cfg['telegram_chat_id'], msg)
            salvar_sinal(sinal)
        else:
            print("  😴 Mercado lateral (Sem sinal)")

        intervalo = cfg.get("intervalo_min", 5)
        print(f"  ⏳ Aguardando {intervalo} min (config do painel)...")
        time.sleep(intervalo * 60)
        
    except Exception as e:
        print(f"  ❌ Erro no loop: {e}")
        time.sleep(60)
