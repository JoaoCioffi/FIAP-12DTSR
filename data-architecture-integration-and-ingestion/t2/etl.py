from docker_handler import dockerComposeUp,dockerComposeDown
from cassandra.auth import PlainTextAuthProvider
from stablish_ports import awaitsService
from pymongo import MongoClient, errors
from cassandra.cluster import Cluster
from read_csv_files import readFiles
from mysql.connector import Error
from params import params
import mysql.connector
import json
import time

# opção para o usuário
instruction="""
 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
                        ::: ETL Process :::

>> Deseja interromper automaticamente a docker ao final da execução do script (S/N)?

Obs: ao interromper não será possível validar as tabelas/docs criadoss através de um DB_Client
via CLI/GUI (ex: Beekeeper Studio, DBeaver, HeidiSQL, Mongosh, cqlsh, dentre outras)...

>> Insira aqui sua resposta: """
userInput=input(instruction)
if userInput.upper() not in ("S","N"):
    print("\nEntrada inválida. Encerrando o programa...")
    exit()

# carrega as variáveis de ambiente
_,credentials=params()

# inicializa o container
dockerComposeUp()

# carrega os dataframes (extraídos dos arquivos .csv)
df_clientes,\
df_produtos,\
df_pedidos,\
df_clientes_concorrente,\
df_produtos_concorrente=readFiles()

""" Rate Limiting / Throttling: limita o número de transações
    por segundo para não sobrecarregar o banco de dados
"""
RATE_LIMITING=0.1

# ------------------------ MySQL ------------------------ #
print('\n','-='*32,'\n','\t\t\t[MySQL Handler]\n')

awaitsService(start=0,stop=15,step=0.6)

try:
    """Estabelece a conexão com o banco de dados."""
    print("\n>> Tentando conectar ao MySQL...")
    cnx=mysql.connector.connect(
        host=credentials["MySQL"]["host"],
        port=credentials["MySQL"]["port"],
        user=credentials["MySQL"]["user"],
        password=credentials["MySQL"]["password"],
        database=credentials["MySQL"]["database"]
    )
    cursor=cnx.cursor()
    print(f"\n🟢 [INFO] Conexão com MySQL estabelecida na porta: {credentials['MySQL']['port']} | database: {credentials['MySQL']['database']}")
    try:
        
        """Executa uma query (DDL)"""
        print("\n⚡ Criando tabelas no MySQL: produtos, clientes, pedidos - [PARTE 01]")
        
        print("\n")
        print(">> Criando a tabela de clientes...")
        createQueryString="""
            CREATE TABLE IF NOT EXISTS `clientes` (
                `id` int NOT NULL AUTO_INCREMENT,
                `cpf` varchar(255) NOT NULL,
                `nome` varchar(255) NOT NULL,
                `endereco` varchar(255),
                `cep` varchar(255),
                `email` varchar(255),
                `telefone` varchar(255),
            PRIMARY KEY (`id`)
            );
        """
        cursor.execute(createQueryString)

        print(">> Criando a tabela de produtos...")
        createQueryString="""
            CREATE TABLE IF NOT EXISTS `produtos` (
                `id` int NOT NULL AUTO_INCREMENT,
                `codigo` varchar(255) NOT NULL,
                `nome` varchar(255) NOT NULL,
                `modelo` varchar(255) NOT NULL,
                `fabricante` varchar(255) NOT NULL,
                `cor` varchar(255),
                `tam` varchar(255),
            PRIMARY KEY (`id`)
            );
        """
        cursor.execute(createQueryString)

        print(">> Criando a tabela de pedidos...")
        createQueryString="""
            CREATE TABLE IF NOT EXISTS `pedidos` (
                `id` int NOT NULL AUTO_INCREMENT,
                `id_cliente` int NOT NULL,
                `cliente` varchar(255) NOT NULL,
                `endereco` varchar(255) NOT NULL,
                `cep` varchar(255) NOT NULL,
                `itens` varchar(255) NOT NULL,
                `qtdes` int,
                `valor_pago` float,
                PRIMARY KEY (`id`),
            FOREIGN KEY (id_cliente) REFERENCES clientes(id)
        );
        """
        cursor.execute(createQueryString)
        
        """Verifica tabelas criadas e registros"""
        print("\n")
        cursor.execute("""SHOW TABLES;""")
        print(f">> Tabelas criadas: {cursor.fetchall()}")
        cursor.execute("""SELECT COUNT(*) FROM clientes;""")
        print(f">> Total de registros (clientes): {cursor.fetchall()}")
        cursor.execute("""SELECT COUNT(*) FROM produtos;""")
        print(f">> Total de registros (produtos): {cursor.fetchall()}")
        cursor.execute("""SELECT COUNT(*) FROM pedidos;""")
        print(f">> Total de registros (pedidos): {cursor.fetchall()}")
        
        """Executa uma query (DML)"""
        print("\n⚡ Inserindo os dados nas tabelas no MySQL: produtos, clientes, pedidos - [PARTE 02]")
        
        print("\n>> Tabela de Clientes:")
        print(df_clientes,'\n')
        for index in range(len(df_clientes)):
            val=tuple(df_clientes.iloc[index].values)
            insertQueryString="""
            INSERT INTO clientes 
            (cpf,nome,endereco,cep,email,telefone)
            VALUES (%s,%s,%s,%s,%s,%s);
            """
            cursor.execute(insertQueryString,val)
            cnx.commit()
            print(f"{val} ⇾ {cursor.rowcount} record inserted...")
            time.sleep(RATE_LIMITING)
        
        print("\n>> Tabela de Produtos:")
        print(df_produtos,'\n')
        for index in range(len(df_produtos)):
            val=tuple(df_produtos.iloc[index].values)
            insertQueryString="""
            INSERT INTO produtos 
            (codigo,nome,modelo,fabricante,cor,tam)
            VALUES (%s,%s,%s,%s,%s,%s);
            """
            cursor.execute(insertQueryString,val)
            cnx.commit()
            print(f"{val} ⇾ {cursor.rowcount} record inserted...")
            time.sleep(RATE_LIMITING)
            
        print("\n>> Tabela de Pedidos:")
        print(df_pedidos,'\n')
        for index in range(len(df_pedidos)):
            val=tuple(df_pedidos.iloc[index].values)
            insertQueryString="""
            INSERT INTO pedidos
            (id_cliente,cliente,endereco,cep,itens,qtdes,valor_pago)
            VALUES (%s,%s,%s,%s,%s,%s,%s);
            """
            cursor.execute(insertQueryString,val)
            cnx.commit()
            print(f"{val} ⇾ {cursor.rowcount} record inserted...")
            time.sleep(RATE_LIMITING)
        
        """Verifica registros"""
        print("\n")
        cursor.execute("""SELECT COUNT(*) FROM clientes;""")
        print(f">> Total de registros (clientes): {cursor.fetchall()}")
        cursor.execute("""SELECT COUNT(*) FROM produtos;""")
        print(f">> Total de registros (produtos): {cursor.fetchall()}")
        cursor.execute("""SELECT COUNT(*) FROM pedidos;""")
        print(f">> Total de registros (pedidos): {cursor.fetchall()}")
            
        """Executa uma query (DML)"""
        print("\n⚡ Importando dados do concorrente: produtos, clientes - [PARTE 03]")
        
        print("\n>> Tabela de Produtos:")
        print(df_produtos_concorrente,'\n')
        for index in range(len(df_produtos_concorrente)):
            val=tuple(df_produtos_concorrente.iloc[index].values)
            insertQueryString="""
            INSERT INTO produtos 
            (codigo,nome,modelo,fabricante,cor,tam)
            VALUES (%s,%s,%s,%s,%s,%s);
            """
            cursor.execute(insertQueryString,val)
            cnx.commit()
            print(f"{val} ⇾ {cursor.rowcount} record inserted...")
            time.sleep(RATE_LIMITING)
        
        print("\n>> Tabela de Clientes:")
        print(df_clientes_concorrente,'\n')
        for index in range(len(df_clientes_concorrente)):
            val=tuple(df_clientes_concorrente.iloc[index].values)
            insertQueryString="""
            INSERT INTO clientes 
            (cpf,nome,endereco,cep,email,telefone)
            VALUES (%s,%s,%s,%s,%s,%s);
            """
            cursor.execute(insertQueryString,val)
            cnx.commit()
            print(f"{val} ⇾ {cursor.rowcount} record inserted...")
            time.sleep(RATE_LIMITING)
        
        """Verifica registros"""
        print("\n")
        cursor.execute("""SELECT COUNT(*) FROM clientes;""")
        print(f">> Total de registros (clientes): {cursor.fetchall()}")
        cursor.execute("""SELECT COUNT(*) FROM produtos;""")
        print(f">> Total de registros (produtos): {cursor.fetchall()}")
        cursor.execute("""SELECT COUNT(*) FROM pedidos;""")
        print(f">> Total de registros (pedidos): {cursor.fetchall()}")

    except Error as e:
        print(f"\n🔴 [ERROR] Erro ao criar as tabelas no MySQL:\n{e}")
        cnx.rollback()

except Error as e:
    print(f"\n🔴 [ERROR] Erro ao conectar ao MySQL:\n{e}")
    cnx.close()
    print("\n🔴 [INFO] Conexão com MySQL encerrada...")
    raise
finally:
    cnx.close()
    print("\n🔴 [INFO] Conexão com MySQL encerrada...\n")
    
# ------------------------ MongoDB ------------------------ #
print('\n','-='*32,'\n','\t\t\t[MongoDB Handler]\n')

awaitsService(start=0,stop=2,step=0.25)

client=None
try:
    """Estabelece a conexão com o banco de dados."""
    client=MongoClient(
                        host=credentials["MongoDB"]["host"],
                        port=credentials["MongoDB"]["port"],
                        username=credentials["MongoDB"]["user"],
                        password=credentials["MongoDB"]["password"],
                        authSource=credentials["MongoDB"]["authsource"],
                        serverSelectionTimeoutMS=3000
    )
    client.admin.command('ping') # força verificação da conexão (ping no servidor)
    db=client[credentials['MongoDB']['database']]
    print(f"\n🟢 [INFO] Conexão com MongoDB estabelecida na porta: {credentials['MongoDB']['port']} | database: {credentials['MongoDB']['database']}")

    print("\n⚡ Criando collections no MongoDB: produtos, clientes, pedidos - [PARTE 01]")

    print("\n")
    print(">> Criando a collection de clientes...")
    db.create_collection(name='clientes')

    print(">> Criando a collection de produtos...")
    db.create_collection(name='produtos')

    print(">> Criando a collection de pedidos...")
    db.create_collection(name='pedidos')

    """Verifica collections criadas e registros"""
    print("\n")
    print(f">> Collections criadas: {db.list_collection_names()}")
    print(f">> Total de documentos/registros (clientes): {db.clientes.count_documents({})}")
    print(f">> Total de documentos/registros (produtos): {db.produtos.count_documents({})}")
    print(f">> Total de documentos/registros (pedidos): {db.pedidos.count_documents({})}")

    print("\n⚡ Inserindo documentos no MongoDB: produtos, clientes, pedidos - [PARTE 02]")
    
    print("\n>> Collection de Clientes:")
    counter=0
    for registry in df_clientes.to_dict(orient='records'):
        counter+=1
        collection=db["clientes"]
        print(f"{json.dumps(registry,indent=4,ensure_ascii=False)}\n\n{counter} document(s) inserted...\n")
        collection.insert_one(registry)
        time.sleep(RATE_LIMITING)
    print('\n')
    """Cria um índice na collection"""
    collection.create_index([
        ('cpf',1),('nome',1),('endereco',1),
        ('cep',1),('email',1),('telefones',1)
    ],unique=True)

    print("\n>> Collection de Produtos:")
    counter=0
    df_produtos_cp=df_produtos.copy().astype({
            'cor':'object',
            'tam':'object'
    })
    for registry in df_produtos.to_dict(orient='records'):
        counter+=1
        collection=db["produtos"]
        print(f"{json.dumps(registry,indent=4,ensure_ascii=False)}\n\n{counter} document(s) inserted...\n")
        collection.insert_one(registry)
        time.sleep(RATE_LIMITING)
    print('\n')
    """Cria um índice na collection"""
    collection.create_index([
        ('codigo',1),('nome',1),('modelo',1),
        ('fabricante',1),('cor',1),('tam',1)
    ],unique=True)

    print("\n>> Collection de Pedidos:")
    counter=0
    df_pedidos_cp=df_pedidos.copy().astype({
            'id_cliente':'int',
            'qtdes':'int',
            'valor_pago':'float'
    })
    for registry in df_pedidos_cp.to_dict(orient='records'):
        counter+=1
        collection=db["pedidos"]
        print(f"{json.dumps(registry,indent=4,ensure_ascii=False)}\n\n{counter} document(s) inserted...\n")
        collection.insert_one(registry)
        time.sleep(RATE_LIMITING)
    print('\n')
    """Cria um índice na collection"""
    collection.create_index([
        ('id_cliente',1),('cliente',1),('endereco',1),
        ('cep',1),('itens',1),('qtdes',1),('valor_pago',1)
    ],unique=True)

    """Verifica registros"""
    print("\n")
    print(f">> Total de documentos/registros (clientes): {db.clientes.count_documents({})}")
    print(f">> Total de documentos/registros (produtos): {db.produtos.count_documents({})}")
    print(f">> Total de documentos/registros (pedidos): {db.pedidos.count_documents({})}")


except errors.ConnectionFailure as e:
    raise RuntimeError(f"\n🔴 [ERROR] Falha ao conectar: {e}")
finally:
    # Encerra a conexão, se aberta
    if client:
        client.close()
        print("\n🔴 [INFO] Conexão com MongoDB encerrada...\n")

# ---------------------------- Cassandra ---------------------------- #
print('\n','-='*32,'\n','\t\t\t[Cassandra Handler]\n')

awaitsService(start=0,stop=30,step=0.6)

# Configurações do cluster
auth_provider=PlainTextAuthProvider(
                                    username=credentials["Cassandra"]["user"],
                                    password=credentials["Cassandra"]["password"]
                                    )
cluster=Cluster(['localhost'],port=credentials["Cassandra"]["port"],auth_provider=auth_provider)
try:
    """Estabelece a conexão com o banco de dados."""
    print("\n>> Tentando conectar ao Cassandra...")
    session=cluster.connect()
    
    if session:
        
        print(f"\n🟢 [INFO] Conexão com Cassandra estabelecida na porta: {credentials['Cassandra']['port']} | cluster: {credentials['Cassandra']['cluster']} | datacenter: {credentials['Cassandra']['datacenter']}")
        print(f"\n>> Criando keyspace...")
        
        """Cria um Keyspace"""
        keyspace=credentials["Cassandra"]["keyspace"]
        createKeyspaceCQL = f"""
        CREATE KEYSPACE IF NOT EXISTS {keyspace}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}
        """
        session.execute(createKeyspaceCQL)

        print(f"\n[INFO] Keyspace `{keyspace}` criado...")

        """Usando o Keyspace criado"""
        session.set_keyspace(keyspace)

        """Criando as tabelas"""
        print("\n⚡ Criando tabelas no Cassandra: produtos, clientes, pedidos - [PARTE 01]")

        print("\n")
        print(">> Criando a tabela de clientes...")
        createQueryString="""
            CREATE TABLE IF NOT EXISTS clientes (
                id int PRIMARY KEY,
                cpf text,
                nome text,
                endereco text,
                cep text,
                email text,
                telefone text
            );
        """
        session.execute(createQueryString)

        print(">> Criando a tabela de produtos...")
        createQueryString="""
            CREATE TABLE IF NOT EXISTS produtos (
                id int PRIMARY KEY,
                codigo text,
                nome text,
                modelo text,
                fabricante text,
                cor text,
                tam text
        );
        """
        session.execute(createQueryString)

        print(">> Criando a tabela de pedidos...")
        createQueryString="""
            CREATE TABLE IF NOT EXISTS pedidos (
                id int PRIMARY KEY,
                id_cliente int,
                cliente text,
                endereco text,
                cep text,
                itens text,
                qtdes int,
                valor_pago float
            );
        """
        session.execute(createQueryString)

        """Verifica tabelas criadas"""
        print("\n")
        metadata=cluster.metadata
        print(f">> Tabelas criadas: {metadata.keyspaces[keyspace].tables.keys()}")
        result=session.execute("""SELECT COUNT(*) FROM clientes;""")
        print(f">> Total de registros (clientes): {list(result)[0][0]}")
        result=session.execute("""SELECT COUNT(*) FROM produtos;""")
        print(f">> Total de registros (produtos): {list(result)[0][0]}")
        result=session.execute("""SELECT COUNT(*) FROM pedidos;""")
        print(f">> Total de registros (pedidos): {list(result)[0][0]}")

        """Inserindo registros"""
        print("\n⚡ Inserindo os dados nas tabelas no Cassandra: produtos, clientes, pedidos - [PARTE 02]")
        
        print("\n>> Tabela de Clientes:")
        print(df_clientes.to_string(index=False),'\n')
        ids=[index+1 for index in df_clientes.index]
        for index in range(len(df_clientes)):
            dfRowValues=tuple(df_clientes.iloc[index].values)
            val=[ids[index]]
            for v in dfRowValues:
                val.append(v)
            val=tuple(val)
            insertQueryString="""
            INSERT INTO clientes (id,cpf,nome,endereco,cep,email,telefone)
            VALUES (%s,%s,%s,%s,%s,%s,%s);"""
            session.execute(query=insertQueryString,parameters=val)
            print(f"{val} ⇾ 1 record inserted...")
            time.sleep(RATE_LIMITING)

        print("\n>> Tabela de Produtos:")
        print(df_produtos.to_string(index=False),'\n')
        ids=[index+1 for index in df_produtos.index]
        for index in range(len(df_produtos)):
            dfRowValues=tuple(df_produtos.iloc[index].values)
            val=[ids[index]]
            for v in dfRowValues:
                val.append(v)
            val=tuple(val)
            insertQueryString="""
            INSERT INTO produtos (id,codigo,nome,modelo,fabricante,cor,tam)
            VALUES (%s,%s,%s,%s,%s,%s,%s);"""
            session.execute(query=insertQueryString,parameters=val)
            print(f"{val} ⇾ 1 record inserted...")
            time.sleep(RATE_LIMITING)
        
        print("\n>> Tabela de Pedidos:")
        print(df_pedidos.to_string(index=False),'\n')
        df_pedidos_cp=df_pedidos.copy().astype({
            'id_cliente':'int',
            'qtdes':'int',
            'valor_pago':'float'
        })
        ids=[index+1 for index in df_pedidos_cp.index]
        for index in range(len(df_pedidos_cp)):
            dfRowValues=tuple(df_pedidos_cp.iloc[index].values)
            val=[ids[index]]
            for v in dfRowValues:
                val.append(v)
            val=tuple(val)
            insertQueryString="""
            INSERT INTO pedidos (id,id_cliente,cliente,endereco,cep,itens,qtdes,valor_pago)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
            session.execute(query=insertQueryString,parameters=val)
            print(f"{val} ⇾ 1 record inserted...")
            time.sleep(RATE_LIMITING)
        
        """Verifica registros"""
        print("\n")
        result=session.execute("""SELECT COUNT(*) FROM clientes;""")
        print(f">> Total de registros (clientes): {list(result)[0][0]}")
        result=session.execute("""SELECT COUNT(*) FROM produtos;""")
        print(f">> Total de registros (produtos): {list(result)[0][0]}")
        result=session.execute("""SELECT COUNT(*) FROM pedidos;""")
        print(f">> Total de registros (pedidos): {list(result)[0][0]}")
            
except Exception as e:
    print(f"\n🔴 [ERROR] Falha ao conectar: {e}")
finally:
    if session:
        session.shutdown()
    cluster.shutdown()
    print("\n🔴 [INFO] Cluster Cassandra encerrado...\n")


# ------------------------ End of Execution ------------------------ #
# finaliza o container
print('\n','-='*32)
if userInput.upper()=="S":
    dockerComposeDown()
    print("\n[INFO] Execução do programa finalizada.\n")
else:
    print("\n[INFO] Execução do programa finalizada. Docker ainda ativo...\n")