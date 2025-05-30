from handlers import MySQL, MongoDB  # Cassandra pode ser adicionado depois
import subprocess
import json
import time

def carregar_schema(caminho="schema.json"):
    """Lê o arquivo JSON de schema e retorna o dicionário"""
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------- MySQL ----------
def criar_tabelas_mysql(schema):
    print("\n💾 Criando tabelas no MySQL...")
    mysql = MySQL()
    for tabela_nome, tabela_schema in schema.items():
        mysql.create(tabela_schema, tabela_nome)
    mysql.close()

def inserir_dados_mysql(schema):
    print("\n📥 Inserindo dados no MySQL...")
    mysql = MySQL()
    mysql.insert(schema["Clientes"], "Clientes", "data/clientes_sample.csv")
    mysql.insert(schema["Produtos"], "Produtos", "data/produtos_sample.csv")
    mysql.insert(schema["Pedidos"], "Pedidos", "data/pedidos_sample.csv")
    mysql.close()

def importar_concorrente_mysql(schema):
    print("\n🏢 Importando dados do concorrente no MySQL...")
    mysql = MySQL()
    mysql.update(schema["Clientes"], "Clientes", "data/clientes_concorrente.csv")
    mysql.update(schema["Produtos"], "Produtos", "data/produtos_concorrente.csv")
    mysql.close()

# ---------- MongoDB ----------
def iniciar_docker_mongodb():
    print("\n🐳 Iniciando container do MongoDB via Docker Compose...")
    try:
        subprocess.run(["docker", "compose", "up", "-d"], check=True)
        time.sleep(5)  # Aguarda alguns segundos para o Mongo estar de pé
        print("✅ Docker MongoDB iniciado com sucesso.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao iniciar o Docker: {e}")

def criar_colecoes_mongo(schema):
    print("\n💾 Criando coleções no MongoDB...")
    mongo = MongoDB()
    for collection_name, collection_schema in schema.items():
        mongo.create(collection_schema, collection_name)
    mongo.close()

def inserir_dados_mongo(schema):
    print("\n📥 Inserindo documentos no MongoDB...")
    mongo = MongoDB()
    mongo.insert(schema["Clientes"], "Clientes", "data/clientes_sample.csv")
    mongo.insert(schema["Produtos"], "Produtos", "data/produtos_sample.csv")
    mongo.insert(schema["Pedidos"], "Pedidos", "data/pedidos_sample.csv")
    mongo.close()

def importar_concorrente_mongo(schema):
    print("\n🏢 Importando dados do concorrente no MongoDB...")
    mongo = MongoDB()
    mongo.update(schema["Clientes"], "Clientes", "data/clientes_concorrente.csv")
    mongo.update(schema["Produtos"], "Produtos", "data/produtos_concorrente.csv")
    mongo.close()

# ---------- Execução ----------
def main():
    print("🔄 Iniciando processo ETL...\n")
    schema = carregar_schema()

    # MySQL
    print('\n','-='*32,'\n','\t\t\t[MySQL Handler]')
    criar_tabelas_mysql(schema)
    inserir_dados_mysql(schema)
    importar_concorrente_mysql(schema)

    # MongoDB
    print('\n','-='*32,'\n','\t\t\t[MongoDB Handler]')
    iniciar_docker_mongodb()
    criar_colecoes_mongo(schema)
    inserir_dados_mongo(schema)
    importar_concorrente_mongo(schema)

    print("\n✅ Processo concluído com sucesso.")

if __name__ == "__main__":
    main()
