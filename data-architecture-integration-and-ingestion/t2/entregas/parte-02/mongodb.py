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
db = client['shoes_world']

# Coleções
produtos_col = db["Produtos"]
clientes_col = db["Clientes"]
pedidos_col = db["Pedidos"]

# Dados de Produtos
produtos_data = [
    {
        "produto_id": 1,
        "codigo": "SH001",
        "nome": "Tênis Modelo 1",
        "modelo": "M1",
        "fabricante": "MarcaX",
        "cores": ["Preto", "Branco"],
        "tamanhos": [38, 39, 40]
    },
    {
        "produto_id": 2,
        "codigo": "SH002",
        "nome": "Tênis Modelo 2",
        "modelo": "M2",
        "fabricante": "MarcaX",
        "cores": ["Preto", "Branco"],
        "tamanhos": [38, 39, 40]
    },
    {
        "produto_id": 3,
        "codigo": "SH003",
        "nome": "Tênis Modelo 3",
        "modelo": "M3",
        "fabricante": "MarcaX",
        "cores": ["Preto", "Branco"],
        "tamanhos": [38, 39, 40]
    },
    {
        "produto_id": 4,
        "codigo": "SH004",
        "nome": "Tênis Modelo 4",
        "modelo": "M4",
        "fabricante": "MarcaX",
        "cores": ["Preto", "Branco"],
        "tamanhos": [38, 39, 40]
    },
    {
        "produto_id": 5,
        "codigo": "SH005",
        "nome": "Tênis Modelo 5",
        "modelo": "M5",
        "fabricante": "MarcaX",
        "cores": ["Preto", "Branco"],
        "tamanhos": [38, 39, 40]
    }
]

# Dados de Clientes
clientes_data = [
    {
        "cliente_id": 1,
        "cpf": "1",
        "nome": "Cliente 1",
        "endereco": "Rua 1",
        "cep": "12345-101",
        "email": "cliente1@email.com",
        "telefones": ["1190000001", "112345671"]
    },
    {
        "cliente_id": 2,
        "cpf": "2",
        "nome": "Cliente 2",
        "endereco": "Rua 2",
        "cep": "12345-102",
        "email": "cliente2@email.com",
        "telefones": ["1190000002", "112345672"]
    },
    {
        "cliente_id": 3,
        "cpf": "3",
        "nome": "Cliente 3",
        "endereco": "Rua 3",
        "cep": "12345-103",
        "email": "cliente3@email.com",
        "telefones": ["1190000003", "112345673"]
    },
    {
        "cliente_id": 4,
        "cpf": "4",
        "nome": "Cliente 4",
        "endereco": "Rua 4",
        "cep": "12345-104",
        "email": "cliente4@email.com",
        "telefones": ["1190000004", "112345674"]
    },
    {
        "cliente_id": 5,
        "cpf": "5",
        "nome": "Cliente 5",
        "endereco": "Rua 5",
        "cep": "12345-105",
        "email": "cliente5@email.com",
        "telefones": ["1190000005", "112345675"]
    }
]

# Dados de Pedidos
pedidos_data = [
    {
        "pedido_id": 1,
        "cliente_id": 1,
        "endereco_entrega": "Entrega Rua 1",
        "cep_entrega": "12345-201",
        "itens": [101, 102],
        "quantidades": [1, 2],
        "valor_pago": 209.90
    },
    {
        "pedido_id": 2,
        "cliente_id": 2,
        "endereco_entrega": "Entrega Rua 2",
        "cep_entrega": "12345-202",
        "itens": [102, 103],
        "quantidades": [1, 2],
        "valor_pago": 219.90
    },
    {
        "pedido_id": 3,
        "cliente_id": 3,
        "endereco_entrega": "Entrega Rua 3",
        "cep_entrega": "12345-203",
        "itens": [103, 104],
        "quantidades": [1, 2],
        "valor_pago": 229.90
    },
    {
        "pedido_id": 4,
        "cliente_id": 4,
        "endereco_entrega": "Entrega Rua 4",
        "cep_entrega": "12345-204",
        "itens": [104, 105],
        "quantidades": [1, 2],
        "valor_pago": 239.90
    },
    {
        "pedido_id": 5,
        "cliente_id": 5,
        "endereco_entrega": "Entrega Rua 5",
        "cep_entrega": "12345-205",
        "itens": [105, 106],
        "quantidades": [1, 2],
        "valor_pago": 249.90
    }
]

# Inserções
produtos_col.insert_many(produtos_data)
clientes_col.insert_many(clientes_data)
pedidos_col.insert_many(pedidos_data)

print("Dados inseridos com sucesso no MongoDB!")