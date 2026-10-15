# 🟡 Agente XAUUSD v1 — Trading Bot em tempo real

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-black.svg)

Bot Python que coleta o preço do ouro (**XAU/USD**) a cada 1 minuto, salva o histórico em CSV e expõe um dashboard web com gráfico em tempo real.

> Primeiro projeto. Mantido como registro de onde isso começou — não é código de produção.

## Como rodar (2 terminais)

**Terminal 1 — Coletor**

```bash
python3 coletor.py
```

**Terminal 2 — Servidor**

```bash
uvicorn servidor:app --reload
```

API + site em `http://localhost:8000`

## Estrutura

| Arquivo | Papel |
|---|---|
| `coletor.py` | coleta o preço do ouro a cada 1 minuto |
| `servidor.py` | API FastAPI + frontend |
| `painel.html` | dashboard com gráfico em tempo real |
| `config.py` | carrega `config.json` + segredos |
| `config.json` | parâmetros públicos: lote, meta, stop, intervalos |
| `dados/` | CSVs de preços, sinais e verificações |

Dependências: `yfinance`, `requests`, `fastapi`, `uvicorn`.

## Segredos

Nenhuma credencial é versionada neste repositório. O token do bot do Telegram e o chat id ficam em **`config_secrets.json`** (ignorado pelo git) ou em variáveis de ambiente:

```bash
export TELEGRAM_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
```

`config.py` mescla `config_secrets.json` sobre os valores padrão de `config.json`.

## Histórico

O repositório foi reescrito em **2026-10-14** para remover um token de bot do Telegram que ficou exposto neste repo público desde março de 2026. Se você clonou antes dessa data, re-clone.
