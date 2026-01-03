
import psutil

nome_processo = "PromAPI.exe"  # Windows
# nome_processo = "firefox"   # Linux

for proc in psutil.process_iter(['pid', 'name']):
    if proc.info['name'] == nome_processo:
        proc.kill()
        print(f"Processo {nome_processo} (PID {proc.pid}) encerrado")


