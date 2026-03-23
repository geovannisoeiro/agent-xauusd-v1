# 🟡 Agente XAUUSD v1 - Trading Bot Real-time

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-black.svg)

Bot Python que coleta preço do ouro (**XAUUSD**) a cada 1 minuto, salva histórico e expõe dashboard web com gráfico em tempo real.

## 🚀 Como rodar (2 terminais)

### **Terminal 1 — Coletor**
```bash
python3 coletor.py

### **Terminal 2 — Coletor**
```bash
uvicorn servidor:app --reload

API + site em  http://localhost:8000 

📁 Estrutura Principal
	•	 coletor.py  — script de coleta 1x/min
	•	 servidor.py  — API FastAPI e frontend web
	•	 config.py  — configuração segura
	•	 .gitignore  — mantém segredos seguros

