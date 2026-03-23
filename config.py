#!/usr/bin/env python3
"""
Config universal para todos scripts. Segredos em config_secrets.json
"""

import json
import os

def carregar_config():
    """Carrega config + segredos"""
    
    # Config padrão (vai pro GitHub)
    config_padrao = {
        'lote': 0.01,
        'meta': 10.0,
        'stop': 20.0,
        'intervalo_min': 5,
        'canal_min': 10,
        'canal_max': 80
    }
    
    # Tentar carregar segredos
    segredos = {}
    if os.path.exists('config_secrets.json'):
        try:
            with open('config_secrets.json', 'r') as f:
                segredos = json.load(f)
        except Exception as e:
            print(f"⚠️ Erro config_secrets: {e}")
    
    # Merge tudo
    config_final = {**config_padrao, **segredos}
    return config_final

# Config global (importe aqui)
CONFIG = carregar_config()
