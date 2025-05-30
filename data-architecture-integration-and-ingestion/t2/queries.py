import mysql.connector
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
import pandas as pd
import json

class MySQL:
    def __init__(self):
        load_dotenv()

        self.conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        self.cursor = self.conn.cursor()

    def _map_dtype(self, dtype):
        mapping = {
            "int": "INT",
            "str": "VARCHAR(255)",
            "float": "FLOAT",
            "list[int]": "JSON",
            "list[str]": "JSON"
        }
        return mapping.get(dtype, "VARCHAR(255)")

    def create(self, table_schema: dict, table_name: str):
        fields = table_schema["fields"]
        primary_key = table_schema["primary_key"]

        columns_sql = []
        for field_name, dtype in fields.items():
            sql_type = self._map_dtype(dtype)
            columns_sql.append(f"`{field_name}` {sql_type}")
        columns_sql.append(f"PRIMARY KEY (`{primary_key}`)")
        columns_str = ",\n  ".join(columns_sql)

        create_statement = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n  {columns_str}\n);"

        self.cursor.execute(create_statement)
        self.conn.commit()
        print(f"✅ Tabela `{table_name}` criada no MySQL.")

    def insert(self, table_schema: dict, table_name: str, csv_path: str):
        fields = table_schema["fields"]
        field_names = list(fields.keys())

        df = pd.read_csv(csv_path)

        # Pré-processa listas como JSON strings
        for field, dtype in fields.items():
            if dtype.startswith("list"):
                df[field] = df[field].apply(lambda x: json.dumps(eval(x)) if not isinstance(x, str) else x)

        # Monta comando SQL de insert
        placeholders = ", ".join(["%s"] * len(field_names))
        columns_str = ", ".join([f"`{col}`" for col in field_names])
        insert_sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"

        # Prepara dados como lista de tuplas
        values = [tuple(row) for row in df[field_names].values]

        self.cursor.executemany(insert_sql, values)
        self.conn.commit()
        print(f"📥 {len(values)} registros inseridos na tabela `{table_name}` com sucesso.")

    def update(self, table_schema: dict, table_name: str, csv_path: str):
        """
        Realiza a carga de dados adicionais (ex: aquisição de concorrente).
        Neste contexto, é funcionalmente igual ao insert().
        """
        print(f"\n🔄 Importando dados do concorrente para `{table_name}`...")
        self.insert(table_schema, table_name, csv_path)

    def close(self):
        self.cursor.close()
        self.conn.close()

class MongoDB:
    def __init__(self):
        load_dotenv()

        username = quote_plus(os.getenv("MONGO_INITDB_ROOT_USERNAME"))
        password = quote_plus(os.getenv("MONGO_INITDB_ROOT_PASSWORD"))

        mongo_uri = f"mongodb://{username}:{password}@localhost:27017/"
        self.client = MongoClient(mongo_uri)
        self.db = self.client["shoes_world"]

    def create(self, table_schema: dict, collection_name: str):
        """Cria uma coleção vazia explicitamente (MongoDB cria on demand, mas forçamos a criação aqui)"""
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            print(f"✅ Coleção `{collection_name}` criada no MongoDB.")
        else:
            print(f"ℹ️ Coleção `{collection_name}` já existe no MongoDB.")

    def insert(self, table_schema: dict, collection_name: str, csv_path: str):
        """Insere documentos na coleção a partir de CSV"""
        df = pd.read_csv(csv_path)

        # Converter campos de lista JSON (list[int], list[str])
        for field, dtype in table_schema["fields"].items():
            if dtype.startswith("list"):
                df[field] = df[field].apply(lambda x: json.loads(x) if isinstance(x, str) else x)

        documents = df.to_dict(orient="records")
        self.db[collection_name].insert_many(documents)
        print(f"📥 {len(documents)} documentos inseridos na coleção `{collection_name}`.")

    def update(self, table_schema: dict, collection_name: str, csv_path: str):
        """Insere dados do concorrente como extensão dos existentes"""
        print(f"\n🔄 Importando dados do concorrente para `{collection_name}` (MongoDB)...")
        self.insert(table_schema, collection_name, csv_path)

    def close(self):
        self.client.close()