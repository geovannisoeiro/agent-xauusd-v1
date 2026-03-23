import yfinance as yf
import requests
import time
from datetime import datetime

TOKEN = "8656452017:AAH--Hf5dcNrhJytjSNtwdcokZpOPWxlFEw"
CHAT_ID = "1029082401"

def enviar_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    if res.status_code == 200:
        print("  📱 Telegram enviado!")
    else:
        print(f"  ❌ Erro Telegram: {res.text}")

print("🤖 Agente V1 iniciado - Lendo Ouro Real (XAU/USD)")
enviar_telegram("🚀 Agente XAU/USD V1 Ligado! Teste de comunicação.")

while True:
    try:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Verificando XAUUSD...")
        
        # Pega dado real do yfinance (Ouro)
        df = yf.download("GC=F", period="1d", interval="1m", progress=False)
        preco_atual = float(df['Close'].iloc[-1].item())
        preco_ant = float(df['Close'].iloc[-2].item())
        
        # Diferença em "pips" (aproximado)
        diff = (preco_atual - preco_ant)
        
        print(f"  💰 Preço Atual: ${preco_atual:.2f}")
        print(f"  📉 Preço Ant: ${preco_ant:.2f}")
        
        # Força sinal pra teste se o preço mexeu minimamente
        if diff > 0:
            sinal = "🟢 COMPRA"
        else:
            sinal = "🔴 VENDA"
            
        msg = f"🚨 SINAL XAU/USD\n\n{sinal}\n💰 Preço: ${preco_atual:.2f}\n📊 Variação: ${diff:.2f}"
        
        print(f"  🎯 Sinal: {sinal}")
        enviar_telegram(msg)
        
        print("  ⏳ Aguardando 5 min...")
        time.sleep(300)
        
    except Exception as e:
        print(f"  ❌ Erro: {e}")
        time.sleep(60)
