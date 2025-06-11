from params import params
from tqdm import tqdm
import numpy as np
import subprocess
import time

# carrega as variáveis de ambiente
_,credentials=params()

def dockerComposeUp():
    print('\n','-='*32)
    print("\n🐳 Iniciando containers via Docker Compose...\n")
    try:
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        print("\n")
        for t in tqdm(np.arange(0,15,0.5),desc="Estabelendo portas",colour='green'):
            time.sleep(1)
        print("\n")
        print(f"🟢 MySQL ⇾ running at localhost:{credentials['MySQL']['port']}")
        print(f"🟢 MongoDB ⇾ running at localhost:{credentials['MySQL']['port']}")
        print(f"🟢 Cassandra ⇾ running at localhost:{credentials['MySQL']['port']}")
        print(f"\n[INFO] Docker iniciado com sucesso.")
    except subprocess.CalledProcessError as e:
        return f"\n[ERROR] Erro ao iniciar o Docker: {e}"

def dockerComposeDown():
    print('\n','-='*32)
    print("\n🐳 Interrompendo containers...\n")
    try:
        subprocess.run(["docker", "compose", "down"], check=True)
        print("\n")
        print("🔴 MySQL ⇾ stopped")
        print("🔴 MongoDB ⇾ stopped")
        print("🔴 Cassandra ⇾ stopped")
        print (f"\n[INFO] Docker finalizado com sucesso.")
    except subprocess.CalledProcessError as e:
        return f"\n[ERROR] Erro ao iniciar o Docker: {e}"