import subprocess

# ----------- Docker com a imagem dos 3 bancos ----------- #
def dockerCompose():
    print("\n🐳 Iniciando containers via Docker Compose...\n")
    try:
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        print("\n")
        return f"\n[INFO] Docker iniciado com sucesso."
    except subprocess.CalledProcessError as e:
        return f"\n[ERROR] Erro ao iniciar o Docker: {e}"