from urllib.parse import quote_plus
from dotenv import load_dotenv
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Obter dados do .env
username = quote_plus(os.getenv("MONGO_INITDB_ROOT_USERNAME"))
password = quote_plus(os.getenv("MONGO_INITDB_ROOT_PASSWORD"))
host = os.getenv("MONGO_INITDB_HOST", "localhost")
port = os.getenv("MONGO_INITDB_PORT", "27017")

# Conexão MongoDB com autenticação
uri = f"mongodb://{username}:{password}@{host}:{port}/"
client = MongoClient(uri)

# Criar banco
db = client['shoes_world']

# Criar coleção Produtos
db.create_collection("Produtos", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["produto_id", "codigo", "nome", "modelo", "fabricante", "cores", "tamanhos"],
        "properties": {
            "produto_id": {"bsonType": "int"},
            "codigo": {"bsonType": "string"},
            "nome": {"bsonType": "string"},
            "modelo": {"bsonType": "string"},
            "fabricante": {"bsonType": "string"},
            "cores": {"bsonType": "array"},
            "tamanhos": {"bsonType": "array"}
        }
    }
})

# Criar coleção Clientes
db.create_collection("Clientes", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["cliente_id", "cpf", "nome", "endereco", "cep", "email", "telefones"],
        "properties": {
            "cliente_id": {"bsonType": "int"},
            "cpf": {"bsonType": "string"},
            "nome": {"bsonType": "string"},
            "endereco": {"bsonType": "string"},
            "cep": {"bsonType": "string"},
            "email": {"bsonType": "string"},
            "telefones": {"bsonType": "array"}
        }
    }
})

# Criar coleção Pedidos
db.create_collection("Pedidos", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["pedido_id", "cliente_id", "endereco_entrega", "cep_entrega", "itens", "quantidades", "valor_pago"],
        "properties": {
            "pedido_id": {"bsonType": "int"},
            "cliente_id": {"bsonType": "int"},
            "endereco_entrega": {"bsonType": "string"},
            "cep_entrega": {"bsonType": "string"},
            "itens": {"bsonType": "array"},
            "quantidades": {"bsonType": "array"},
            "valor_pago": {"bsonType": "double"}
        }
    }
})

print("Banco e coleções criados com sucesso.")