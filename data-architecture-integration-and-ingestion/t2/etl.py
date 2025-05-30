import json
from queries import MySQL

def carregar_schema(caminho="schema.json"):
    """Lê o arquivo JSON de schema e retorna o dicionário"""
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def criar_tabelas(schema):
    """Executa a criação das tabelas no MySQL"""
    print("\n💾 Criando tabelas no MySQL...")

    mysql = MySQL()

    for tabela_nome, tabela_schema in schema.items():
        mysql.create(tabela_schema, tabela_nome)

    mysql.close()

def inserir_dados(schema):
    """Insere os dados de exemplo nos bancos a partir dos arquivos CSV"""
    print("\n📥 Inserindo dados no MySQL...")

    mysql = MySQL()

    mysql.insert(schema["Clientes"], "Clientes", "data/clientes_sample.csv")
    mysql.insert(schema["Produtos"], "Produtos", "data/produtos_sample.csv")
    mysql.insert(schema["Pedidos"], "Pedidos", "data/pedidos_sample.csv")

    mysql.close()

def importar_concorrente(schema):
    print("\n🏢 Importando dados do concorrente...")

    mysql = MySQL()

    mysql.update(schema["Clientes"], "Clientes", "data/clientes_concorrente.csv")
    mysql.update(schema["Produtos"], "Produtos", "data/produtos_concorrente.csv")

    mysql.close()

def main():
    print("🔄 Iniciando processo ETL...\n")
    schema = carregar_schema()
    criar_tabelas(schema)
    inserir_dados(schema)
    importar_concorrente(schema)
    print("\n✅ Processo concluído com sucesso.")

if __name__ == "__main__":
    main()