from dotenv import load_dotenv
import os

load_dotenv()
def params():
    """Aponta o caminho dos arquivos (.csv) e cria um JSON com as credenciais de acesso lidas (.env)"""
    filesPath={
        "original_db":{
            "info":"base de dados original (arquivos .csv criados para raw data)",
            "customers":"./data/clientes.csv",
            "products":"./data/produtos.csv",
            "orders":"./data/pedidos.csv"
        },
        "imported_db":{
            "info":"base de dados importada do concorrente (arquivos .csv criados para imported data)",
            "products":"./data/produtos_concorrente.csv",
            "customers":"./data/clientes_concorrente.csv"
        }
    }

    credentials={
        "MySQL":{
            "host":os.getenv("MYSQL_HOST"),
            "port":int(os.getenv("MYSQL_PORT")),
            "user":os.getenv("MYSQL_USERNAME"),
            "password":os.getenv("MYSQL_PASSWORD"),
            "database":os.getenv("MYSQL_DATABASE")
        },
        "MongoDB":{

        },
        "Cassandra":{
            "datacenter":os.getenv("CASSANDRA_DATA_CENTER"),
            "port":int(os.getenv("CASSANDRA_PORT")),
            "cluster":os.getenv("CASSANDRA_CLUSTER_NAME"),
            "keyspace":os.getenv("CASSANDRA_KEYSPACE"),
            "user":os.getenv("CASSANDRA_USERNAME"),
            "password":os.getenv("CASSANDRA_PASSWORD")
        }
    }

    return filesPath,credentials