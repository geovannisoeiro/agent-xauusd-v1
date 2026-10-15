import subprocess
H = "<!DOCTYPE html><html><head><meta charset='UTF-8'><style>:root{--bg:#0a0a12;--cyan:#06d6a0;--purple:#7c3aed;--pl:#a855f7;--pink:#f72585;--gold:#ffd60a;--text:#e2e8f0;--text2:#94a3b8;--bg2:#0f0f1a;--bg3:#141428;--border:rgba(124,58,237,0.3);}*{margin:0;padding:0;box-sizing:border-box;}body{background:var(--bg);color:var(--text);font-family:Rajdhani,sans-serif;min-height:100vh;padding:20px;}</style></head><body><h1 style='color:var(--cyan);font-size:2rem;margin-bottom:20px'>XAU/USD AGENT - OK!</h1><p style='color:var(--text2)'>Pipeline funcionando. Proximo passo: painel completo.</p></body></html>"
open("painel.html","w").write(H)
subprocess.run(["open","painel.html"])
print("OK! Arquivo criado:", len(H), "bytes")
