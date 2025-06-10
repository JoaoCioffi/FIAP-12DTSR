from docker_handler import dockerCompose
from read_csv_files import readFiles
from mysql.connector import Error
from params import params
import mysql.connector

# inicializa o docker
dockerCompose()

# carrega as variáveis de ambiente
_,credentials=params()

# carrega os dataframes (extraídos dos arquivos .csv)
df_clientes,\
df_produtos,\
df_pedidos,\
df_clientes_concorrente,\
df_produtos_concorrente=readFiles()

# ------------------------ MySQL ------------------------ #
print('\n','-='*32,'\n','\t\t\t[MySQL Handler]\n')
try:
    """Estabelece a conexão com o banco de dados."""
    cnx = mysql.connector.connect(
        host=credentials["MySQL"]["host"],
        port=credentials["MySQL"]["port"],
        user=credentials["MySQL"]["user"],
        password=credentials["MySQL"]["password"],
        database=credentials["MySQL"]["database"]
    )
    cursor = cnx.cursor()
    print("\n🟢 [INFO] Conexão com MySQL estabelecida...")
    try:
        
        """Executa uma query (DDL)"""
        print("\n⚡ Criando tabelas no MySQL: produtos, clientes, pedidos - [PARTE 01]")

        print("\n>> Criando a tabela de clientes...")
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

        print("\n>> Criando a tabela de produtos...")
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

        print("\n>> Criando a tabela de pedidos...")
        createQueryString="""
            CREATE TABLE IF NOT EXISTS `pedidos` (
                `id` int NOT NULL AUTO_INCREMENT,
                `id_cliente` int NOT NULL,
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
        
        cursor.execute("""SHOW TABLES;""")
        print(f"\n>> Tabelas criadas: {cursor.fetchall()}")

        """Executa uma query (DML)"""
        print("\n⚡ Inserindo os dados nas tabelas no MySQL: produtos, clientes, pedidos - [PARTE 02]")
        
        print("\n>> Tabela de Clientes:")
        print(df_clientes,'\n')
        colNames=tuple(df_clientes.columns.values)
        for index in range(len(df_clientes)):
            val=tuple(df_clientes.iloc[index].values)
            insertQueryString="""
            INSERT INTO clientes 
            (cpf,nome,endereco,cep,email,telefone)
            VALUES (%s,%s,%s,%s,%s,%s);
            """
            cursor.execute(insertQueryString,val)
            cnx.commit()
            print(f"{val} ⇾ {cursor.rowcount} record inserted.")

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
    print("\n🔴 [INFO] com MySQL encerrada...\n")