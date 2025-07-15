# Projeto: ETL de Loja de Calçados - Integração de Dados Multibanco 💡

Integrantes:

- Isabelle Matias: RM363495
- João Cioffi: RM364198
- Renan Ambrosini: RM363304
- Rodrigo: RM363289

## Repositório (Github) 💻

Caso queira consultar, este trabalho (T2) está disponível em: https://github.com/JoaoCioffi/FIAP-12DTSR/tree/main/data-architecture-integration-and-ingestion/t2

Também é possível clonar via:

```bash
git clone https://github.com/JoaoCioffi/FIAP-12DTSR.git
```

porém a main branch conterá todos os trabalhos de todas as disciplinas (estando o T2 especificamente em `./data-architecture-integration-and-ingestion/t2` do repo clonado)

## T2 Data Architecture, Integration and Ingestion 📚

Este projeto consiste na modelagem e integração de dados para um sistema de vendas de calçados, utilizando três tecnologias de banco de dados: **MySQL**, **Cassandra** e **MongoDB**.

## Estrutura do Projeto 🏗️

```bash
.                                  # (root)
├── .env.example                   # exemplo/referência de arquivo a ser lido para criar o .env
├── README.md                      # este arquivo
├── data                           # base de dados / arquivo brutos (.csv)
│   ├── clientes_concorrente.csv   # base de dados importada do concorrente (clientes - .csv - parte 03)
│   ├── cliente.csv                # base de dados inicial (clientes - .csv - partes 01, 02)
│   ├── pedidos.csv                # base de dados inicial (pedidos - .csv - partes 01, 02)
│   ├── produtos_concorrente.csv   # base de dados importada do concorrente (produtos - .csv - parte 03)
│   └── produtos.csv               # base de dados inicial (produtos - .csv - partes 01, 02)
├── docker-compose.yaml            # arquivo yaml para buildar e instanciar as imagens (docker containers)
├── docker_handler.py              # handler docker para python (instancia o docker através de um subprocess)
│
├── etl.py                         # script que lê cada um dos arquivos (.csv), e carrega em cada uma das bases (processo ETL)
│                                  # Obs: ESTE É O SCRIPT PRINCIPAL! NÃO EXECUTE NENHUM OUTRO ALÉM DELE!
│
├── install_requirements.ipynb     # jupyter notebook para troubleshooting caso alguma lib não funcionar adequadamente
├── params.py                      # script que carrega as variáveis de ambiente de cada banco e aponta para os arquivos .csv
├── read_csv_files.py              # script que carrega os .csv num dataframe estruturado (Pandas)
├── requirements.txt               # lista todas as dependências/libs do projeto
└── stablish_ports.py              # força um temporizador para aguardar os containers estabilizarem e portas estarem disponiveis
```

## Configuração de Ambiente ⚙️

- Requisitos:
  - ter Python previamente instalado (e.g Python 3.11) => https://www.python.org/downloads/
    - **⚠️ OBS:** se atente para ter uma v.Python < 3.12 (algumas libs não estão disponíveis para a versão mais atual dele e o projeto não irá funcionar!)
  - ter pip previamente instalado (e.g pip 25.1.1) => https://pypi.org/project/pip/
  - ter Docker previamente instalado (e.g Docker version 28.1.1) => https://www.docker.com
- Criar e ativar um venv (virtaul environment) com python:
  - abra um terminal na root deste projeto e rode: `python -m venv .venv`, em que `.venv` é o nome dado ao seu virtualenv (pode ser arbitrário no formato `python -m venv <your_venv_name_here>`)
  - no mesmo terminal, ative o venv criado:
    - Win: `.\.venv\Scripts\Activate.ps1`
    - Linux: `source .venv/bin/activate`
    - Obs: para desativar (em qualquer um dos OS, apenas digite no terminal `deactivate`)
- Instalar dependências pip (package installer for Python):
  - com o venv ativo, execute no terminal: `pip install -r ./requirements.txt`
- Variáveis de ambiente:
  - as variáveis de ambiente estão no arquivo `.env.example`. Elas estão comentadas quando deve-se ou não ser definidas pelo usuário (ou por quem irá rodar o projeto). Atente-se a isso!
  - para defini-las, crie um novo arquivo no mesmo nível de disco em que está o arquivo anterior, porém nomeando-o para `.env` apenas
  - copie todo o conteúdo de `.env.example` para dentro de `.env` e altere os campos necessários.
  - variáveis como por exemplo `your_db_name_here` significam que você mesmo pode atribuir um valor que achar válido (arbitrário)

## Executando o projeto (ETL) ⌛

Para rodar o projeto, abra um terminal na root e digite `python .\etl.py`. O script terá uma instrução com uma observação. Atente-se a isso! Caso a entrada for inválida, a execução do script será terminada automaticamente. Esta instrução basicamente dá a escolha para o usuário sobre interromper os containers ou deixá-los ativos após o encerramento do processo ETL.

Durante a execução (caso a entrada for válida, e.g: "s", "S", "n", "N"), você verá uma "barra de carregamento" do processo para cada banco.
Isso foi implementado de forma intencional, pois verificou-se que mesmo com o output do terminal exibindo o status de "running" para cada um dos containeres, ainda sim não era possível acessar as portas individualmente, pois com os logs de cada serviço elas ainda estavam sendo estabelecidas. Portanto, é necessário aguardar e estabilização do serviço até que cada um dos bancos esteja 100% disponível.

O script faz a leitura individualmente de cada arquivo .csv e insere em cada um dos bancos e está dividido na seguinte forma:

- MySQL:
  - criação das tabelas 'clientes', 'produtos' e 'pedidos' $\rightarrow$ **Parte 01** deste trabalho
  - inserção dos dados nas tabelas 'clientes', 'produtos' e 'pedidos', linha a linha, vindos de `clientes.csv`, `produtos.csv` e `pedidos.csv` $\rightarrow$ **Parte 02** deste trabalho
  - inserção dos dados nas tabelas 'clientes' e 'produtos', linha a linha, vindos de `clientes_concorrentes.csv` e `produtos_concorrentes.csv` $\rightarrow$ **Parte 03** deste trabalho
- MongoDB:
  - criação das collections 'clientes', 'produtos' e 'pedidos' $\rightarrow$ **Parte 01** deste trabalho
  - inserção de registros/documentos nas collections 'clientes', 'produtos' e 'pedidos', linha a linha, vindos de `clientes.csv`, `produtos.csv` e `pedidos.csv` $\rightarrow$ **Parte 02** deste trabalho
- Cassandra:
  - criação das tabelas 'clientes', 'produtos' e 'pedidos' $\rightarrow$ **Parte 01** deste trabalho
  - inserção dos dados nas tabelas 'clientes', 'produtos' e 'pedidos', linha a linha, vindos de `clientes.csv`, `produtos.csv` e `pedidos.csv` $\rightarrow$ **Parte 02** deste trabalho

Após passar por cada um dos handlers de cada banco, o script será finalizado (fechando apenas a conexão do python com o banco), estando os containers ainda rodando (ativos) a depender da escolha inicial do usuário (via instrução)

OBS: Caso os containers estejam ainda ativos, é possível acessá-los diretamente para validar os dados/registros inseridos e tabelas/collections criadas:

### 1. MySQL:

O container do MySQL pode ser acessado tanto via shell/CLI, quanto por GUI (Ex: Beekeeper Studio, DBeaver, dentre outros). Essas ferramentas geralmente fornecem uma interface em que será necessário inserir os parâmetros como host, porta, usuário e senha (disponíveis no .env criado).

Para acessar via terminal (CLI), insira no terminal:

```bash
docker exec -it mysql mysql -u root -p
```

Ele pedirá sua senha (a mesma que foi definida no .env).

### 2. MongoDB:

O MongoDB contém o shell nativo (mongosh). Para acessá-lo, abra um terminal e execute:

```bash
docker exec -it mongo mongosh -u root -p sua_senha --authenticationDatabase admin
```

estando a senha no .env criado

### 3. Cassandra:

Da mesma forma que temos no MongoDB, o container do Cassandra também permite um acesso direto via CLI. Para isso, abra um terminal e execute:

```bash
docker exec -it cassandra cqlsh -u cassandra -p cassandra
```

Tanto o shell do cassandra quanto o do mongo permite você criar tabelas/collections e inserir os dados diretamente, já que o acesso via command line é direto por um admin user.

## Boas práticas após validação e finalização da execução do projeto ℹ️

Para garantir que não haja nenhuma persistência de dados em disco do que foi executado, podemos executar algumas boas práticas:

### Removendo dependências PIP 🐍

Para desinstalar um módulo python, abra o terminal e execute:

```bash
pip3 uninstall <package-name>
```

onde `<package-name>` é o nome da dependência que foi instalada (veja no requirements.txt o nome correto da lib para poder desinstalar)

### Interrompendo containers, excluindo volumes e excluindo imagens 🐋

#### 1. Interrompendo um container ativo:

Caso o script do etl tenha terminado porém os containeres estejam ainda rodando, abra um terminal (na root do projeto) e rode:

```bash
docker compose down
```

Atenção! Deve estar na root, pois o `docker compose` depende do `docker-compose.yaml` para receber a instrução

#### 2. Excluindo volumes:

Para listar volumes criados:

```bash
docker volume ls
```

Caso queira excluir múltiplos volumes, pode passar eles todos de uma só vez:

```bash
# Exemplo
docker volume rm t2_cassandra_data t2_mongo_data t2_mysql_data
```

em que "t2_cassandra_data", "t2_mongo_data" e "t2_mysql_data" foram os nomes que criamos para os volumes dentro do `docker-compose.yaml`

#### 2. Excluindo imagens:

Infelizmente as imagens para serem excluídas precisam ser pelo ID (gerado por hash pelo docker), o que requer um trabalho um pouco mais manual (existe uma forma automática de remover todas elas de uma só vez, mas pode acabar excluindo uma imagem indesejada). Então para excluirmos exatamente as imagens que criamos para este trabalho (T2), vamos primeiro listar as imagens com:

```bash
docker image ls
```

e você verá algo como

```txt
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
mongo        latest    98028cf281bb   8 days ago     1.2GB
mysql        latest    072f96c2f1eb   8 weeks ago    1.17GB
cassandra    latest    2d241468ad9d   2 months ago   581MB
```

Desta forma, temos o "IMAGE ID" de cada uma delas. Para excluir é simples: copie individualmente cada um dos ids e cole no comando a seguir:

```bash
docker rmi <image-id>
```

substituindo o `<image-id>` pelo id copiado. Então no caso, se quisermos excluir todos estes do exemplo anterior, seria:

```bash
docker rmi 98028cf281bb 072f96c2f1eb 2d241468ad9d
```

e você veria algo como

```txt
Untagged: mongo:latest
Deleted: sha256:98028cf281bb5d49ace5e1ddbd4509e8f1382fe80ef1cf101eeefdc106d76cd4
Untagged: mysql:latest
Deleted: sha256:072f96c2f1ebb13f712fd88d0ef98f2ef9a52ad4163ae67b550ed6720b6d642e
Untagged: cassandra:latest
Deleted: sha256:2d241468ad9d0c091905dddb8d4e5cf4bdfbbfbd6d2acdbd4c7c312e43da93e1
```

o que significa que o docker deletou completamente a imagem

---

Obs: caso o ETL falhe, por qualquer motivo, ainda é possível inserir os dados manualmente considerando que o docker com os 3 containeres esteja rodando e ativo:

### 1. MySQL:

```sql
CREATE TABLE IF NOT EXISTS clientes (
    id INT NOT NULL AUTO_INCREMENT,
    cpf VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255),
    cep VARCHAR(255),
    email VARCHAR(255),
    telefone VARCHAR(255),
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS produtos (
    id INT NOT NULL AUTO_INCREMENT,
    codigo VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    fabricante VARCHAR(255) NOT NULL,
    cor VARCHAR(255),
    tam VARCHAR(255),
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS pedidos (
    id INT NOT NULL AUTO_INCREMENT,
    id_cliente INT NOT NULL,
    cliente VARCHAR(255) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    cep VARCHAR(255) NOT NULL,
    itens VARCHAR(255) NOT NULL,
    qtdes INT,
    valor_pago FLOAT,
    PRIMARY KEY (id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);

INSERT INTO clientes VALUES (NULL, '123.456.789-01', 'João Silva', 'Rua das Palmeiras', '12345-678', 'joao.silva@email.com', '(11) 98765-4321');
INSERT INTO clientes VALUES (NULL, '987.654.321-00', 'Ana Costa', 'Avenida Paulista', '45678-910', 'ana.costa@email.com', '(11) 91234-5678');
INSERT INTO clientes VALUES (NULL, '456.789.123-45', 'Pedro Souza', 'Rua João Pessoa', '78901-234', 'pedro.souza@email.com', '(21) 99123-4567');
INSERT INTO clientes VALUES (NULL, '321.654.987-12', 'Mariana Lima', 'Rua das Acácias', '23456-789', 'mariana.lima@email.com', '(21) 98876-5432');
INSERT INTO clientes VALUES (NULL, '654.987.321-00', 'Lucas Almeida', 'Rua 15 de Novembro', '34567-890', 'lucas.almeida@email.com', '(31) 99111-2233');
INSERT INTO clientes VALUES (NULL, '213.546.879-11', 'Fernanda Oliveira', 'Av. Brasil', '98765-432', 'fernanda.oliveira@email.com', '(31) 99887-4455');
INSERT INTO clientes VALUES (NULL, '543.216.987-32', 'Carlos Pereira', 'Rua do Sol', '65432-123', 'carlos.pereira@email.com', '(41) 99333-2244');
INSERT INTO clientes VALUES (NULL, '876.543.210-65', 'Julia Martins', 'Rua da Paz', '12345-678', 'julia.martins@email.com', '(41) 98877-5566');
INSERT INTO clientes VALUES (NULL, '234.567.891-23', 'Roberto Costa', 'Rua Rio Branco', '87654-321', 'roberto.costa@email.com', '(51) 99222-3344');
INSERT INTO clientes VALUES (NULL, '678.901.234-56', 'Renata Santos', 'Av. Ipiranga', '56789-012', 'renata.santos@email.com', '(51) 99666-7788');
INSERT INTO clientes VALUES (NULL, '432.109.876-43', 'Ricardo Mendes', 'Rua das Flores', '43210-987', 'ricardo.mendes@email.com', '(61) 99122-3344');
INSERT INTO clientes VALUES (NULL, '109.876.543-21', 'Sandra Rocha', 'Rua 7 de Setembro', '65432-109', 'sandra.rocha@email.com', '(61) 99333-2211');
INSERT INTO clientes VALUES (NULL, '890.123.456-78', 'Lívia Ferreira', 'Rua Getúlio Vargas', '78901-432', 'livia.ferreira@email.com', '(71) 99111-4433');
INSERT INTO clientes VALUES (NULL, '210.987.654-32', 'Thiago Santos', 'Av. dos Andradas', '89012-345', 'thiago.santos@email.com', '(71) 99777-6655');
INSERT INTO clientes VALUES (NULL, '765.432.109-87', 'Aline Martins', 'Rua Belo Horizonte', '32109-876', 'aline.martins@email.com', '(81) 99888-1122');
INSERT INTO clientes VALUES (NULL, '543.210.876-90', 'Fábio Almeida', 'Rua dos Três Irmãos', '56789-123', 'fabio.almeida@email.com', '(81) 99333-4455');
INSERT INTO clientes VALUES (NULL, '321.098.765-43', 'Carla Pinto', 'Av. Rio de Janeiro', '65432-890', 'carla.pinto@email.com', '(91) 99222-1144');
INSERT INTO clientes VALUES (NULL, '654.321.987-56', 'Roberta Souza', 'Rua Santo Amaro', '43210-765', 'roberta.souza@email.com', '(91) 99888-7766');
INSERT INTO clientes VALUES (NULL, '987.123.654-32', 'Daniel Rocha', 'Rua Riachuelo', '12345-678', 'daniel.rocha@email.com', '(11) 93333-4455');
INSERT INTO clientes VALUES (NULL, '432.109.876-54', 'Gustavo Lima', 'Av. Santa Catarina', '65432-109', 'gustavo.lima@email.com', '(11) 98888-1234');
INSERT INTO clientes VALUES (NULL, '876.234.567-89', 'Maria Clara', 'Av. Faria Lima', '43210-876', 'mariaclara@email.com', '(21) 92334-5678');
INSERT INTO clientes VALUES (NULL, '345.678.912-34', 'Eduardo Pereira', 'Rua da Liberdade', '76543-210', 'eduardo.pereira@email.com', '(21) 94567-7890');
INSERT INTO clientes VALUES (NULL, '567.890.123-45', 'Vera Lucia', 'Rua São João', '87654-321', 'veralucia@email.com', '(31) 99654-1234');
INSERT INTO clientes VALUES (NULL, '789.012.345-67', 'Luciana Ribeiro', 'Rua das Orquídeas', '23456-789', 'luciana.ribeiro@email.com', '(31) 97888-1122');
INSERT INTO clientes VALUES (NULL, '210.987.654-32', 'Tiago Marques', 'Rua Antônio Carlos', '54321-678', 'tiago.marques@email.com', '(41) 99666-4477');
INSERT INTO clientes VALUES (NULL, '432.098.765-21', 'Paula Souza', 'Av. dos Trabalhadores', '65432-123', 'paula.souza@email.com', '(41) 97777-2233');
INSERT INTO clientes VALUES (NULL, '543.876.109-87', 'Marcelo Santos', 'Rua Paraná', '32109-876', 'marcelo.santos@email.com', '(51) 99888-5544');
INSERT INTO clientes VALUES (NULL, '654.234.987-65', 'Juliana Costa', 'Rua das Acácias', '43210-987', 'juliana.costa@email.com', '(51) 97777-8899');
INSERT INTO clientes VALUES (NULL, '876.234.109-87', 'Luis Carlos', 'Av. São Paulo', '12345-678', 'luis.carlos@email.com', '(61) 99888-2233');
INSERT INTO clientes VALUES (NULL, '987.321.654-00', 'Patrícia Rocha', 'Av. das Américas', '54321-234', 'patricia.rocha@email.com', '(61) 98777-4455');
INSERT INTO produtos VALUES (NULL, 'N31', 'Air Max 90', 'Air Max', 'Nike', '[Preto, Branco, Vermelho, Verde]', '[38,40,41,42]');
INSERT INTO produtos VALUES (NULL, 'A02', 'UltraBoost', 'UltraBoost', 'Adidas', '[Azul, Branco,]', '[40,42]');
INSERT INTO produtos VALUES (NULL, 'N13', 'Free Run 5.0', 'Free', 'Nike', '[Amarelo, Bege]', '[39,40,42,45]');
INSERT INTO produtos VALUES (NULL, 'P84', 'RS-X3', 'RS-X', 'Puma', '[Preto, Branco]', '[40]');
INSERT INTO produtos VALUES (NULL, 'N00', 'React Infinity Run', 'React', 'Nike', '[Cinza, Verde]', '[42,43,45]');
INSERT INTO produtos VALUES (NULL, 'N06', 'Zoom Freak 1', 'Zoom Freak', 'Nike', '[Preto]', '[39,40,41,42]');
INSERT INTO produtos VALUES (NULL, 'M17', 'Wave Rider 24', 'Wave Rider', 'Mizuno', '[Roxo, Verde, Rosa]', '[38,41,42]');
INSERT INTO produtos VALUES (NULL, 'P08', 'Suede Classic', 'Suede', 'Puma', '[Vermelho, Verde, Dourado]', '[39,42]');
INSERT INTO produtos VALUES (NULL, 'A09', 'Primeknit"', 'Primeknit', 'Adidas', '[Preto, Branco]', '[39,40,41,42]');
INSERT INTO produtos VALUES (NULL, 'C10', 'Chuck Taylor"', 'Chuck Taylor', 'Converse', '[Branco, Vermelho, Verde]', '[39,40,41,42,43,44]');
INSERT INTO produtos VALUES (NULL, 'N101-c', 'Air Zoom Pegasus 37', 'Zoom Pegasus', 'Nike', '[Preto, Branco, Vermelho, Azul, Cinza]', '[38,40,41,42]');
INSERT INTO produtos VALUES (NULL, 'A252-c', 'EQT Support', 'EQT', 'Adidas', '[Preto, Branco, Azul, Amarelo]', '[39,40,42]');
INSERT INTO produtos VALUES (NULL, 'R713-c', 'Speed 600', 'Speed 600', 'Reebok', '[Verde, Branco, Cinza, Roxo]', '[38,41,42]');
INSERT INTO produtos VALUES (NULL, 'N164-c', 'React Element 55', 'React', 'Nike', '[Preto, Azul, Verde, Laranja]', '[40,42]');
INSERT INTO produtos VALUES (NULL, 'N75-c', 'Nike Court', 'Air Court', 'Nike', '[Branco, Vermelho, Preto, Cinza]', '[39,41]');
INSERT INTO produtos VALUES (NULL, 'A816-c', 'Asics Gel-Kayano 27', 'Gel-Kayano', 'Asics', '[Amarelo, Azul, Preto]', '[40,42]');
INSERT INTO produtos VALUES (NULL, 'P71-c', 'Clyde', 'Suede', 'Puma', '[Cinza, Branco, Verde]', '[38,40,41]');
INSERT INTO produtos VALUES (NULL, 'N36-c', 'Air Jordan 1', 'Jordan 1', 'Nike', '[Preto, Laranja, Azul]', '[41,42]');
INSERT INTO produtos VALUES (NULL, 'A19-c', 'Runfalcon', 'Runfalcon', 'Adidas', '[Branco, Verde, Amarelo]', '[38,39]');
INSERT INTO produtos VALUES (NULL, 'N20-c', 'Fresh Foam 1080', 'Fresh Foam', ' "New Balance"', '[Vermelho, Preto, Branco, Amarelo]', '[38,40,41]');
INSERT INTO produtos VALUES (NULL, 'A92-c', 'Climacool', 'Climacool', 'Adidas', '[Roxo, Preto, Azul, Vermelho]', '[40,41]');
INSERT INTO produtos VALUES (NULL, 'P22-c', 'Basketball Pro', 'Basketball', 'Puma', '[Cinza, Verde, Laranja]', '[38,40,42]');
INSERT INTO produtos VALUES (NULL, 'N231-c', 'FuelCell Rebel', 'FuelCell', 'New Balance', '[Branco, Vermelho, Azul]', '[39,41,42]');
INSERT INTO produtos VALUES (NULL, 'N249-c', 'Air Max 270', 'Air Max', 'Nike', '[Preto, Branco, Roxo, Azul]', '[38,40]');
INSERT INTO produtos VALUES (NULL, 'N145-c', 'Nike Air Force 1', 'Air Force', 'Nike', '[Vermelho, Branco, Cinza, Preto]', '[39,40,42]');
INSERT INTO produtos VALUES (NULL, 'R216-c', 'Crossfit Nano', 'Crossfit', 'Reebok', '[Amarelo, Preto, Roxo]', '[41,42]');
INSERT INTO produtos VALUES (NULL, 'A971-c', 'Sonic Fury', 'Sonic Fury', 'Asics', '[Azul, Branco, Verde, Cinza]', '[38,40,42]');
INSERT INTO produtos VALUES (NULL, 'N58-c', 'Nike Blazer', 'Blazer', 'Nike', '[Preto, Laranja, Verde, Roxo]', '[39,40]');
INSERT INTO produtos VALUES (NULL, 'I29-c', 'Inov-8 X-Talon', 'X-Talon', 'Inov-8', '[Branco, Cinza, Azul]', '[40,41,42]');
INSERT INTO produtos VALUES (NULL, 'A630-c', 'Adidas Superstar', 'Superstar', 'Adidas', '[Azul, Verde, Preto, Cinza]', '[39,41]');
INSERT INTO pedidos VALUES (NULL, '1', 'João Silva', 'Rua das Palmeiras', '12345-678', 'Tênis Nike Air Max', '1', '450.0');
INSERT INTO pedidos VALUES (NULL, '2', 'Ana Costa', 'Avenida Paulista', '45678-910', 'Tênis Adidas UltraBoost', '2', '889.99');
INSERT INTO pedidos VALUES (NULL, '3', 'Pedro Souza', 'Rua João Pessoa', '78901-234', 'Tênis Puma RS-X3', '1', '350.0');
INSERT INTO pedidos VALUES (NULL, '4', 'Mariana Lima', 'Rua das Acácias', '23456-789', 'Tênis Nike React Infinity', '3', '320.0');
INSERT INTO pedidos VALUES (NULL, '5', 'Lucas Almeida', 'Rua 15 de Novembro', '34567-890', 'Tênis Mizuno Wave Rider 24', '2', '550.63');
INSERT INTO pedidos VALUES (NULL, '7', 'Carlos Pereira', 'Rua do Sol', '65432-123', 'Tênis Converse Chuck Taylor', '1', '250.2');
INSERT INTO pedidos VALUES (NULL, '8', 'Julia Martins', 'Rua da Paz', '12345-678', 'Tênis Nike Zoom Freak', '2', '900.0');
INSERT INTO pedidos VALUES (NULL, '6', 'Fernanda Oliveira', 'Av. Brasil', '98765-432', 'Tênis Adidas EQT Support', '1', '470.5');
INSERT INTO pedidos VALUES (NULL, '10', 'Renata Santos', 'Av. Ipiranga', '56789-012', 'Tênis Reebok Speed 600', '1', '120.0');
INSERT INTO pedidos VALUES (NULL, '7', 'Carlos Pereira', 'Rua do Sol', '65432-123', 'Tênis New Balance Fresh Foam', '1', '700.0');
```

### 2. MongoDB (use mongosh):

```bash
db.createCollection('clientes');
db.createCollection('produtos');
db.createCollection('pedidos');

db.clientes.insertOne({'cpf': '123.456.789-01', 'nome': 'João Silva', 'endereco': 'Rua das Palmeiras', 'cep': '12345-678', 'email': 'joao.silva@email.com', 'telefones': '(11) 98765-4321'})
db.clientes.insertOne({'cpf': '987.654.321-00', 'nome': 'Ana Costa', 'endereco': 'Avenida Paulista', 'cep': '45678-910', 'email': 'ana.costa@email.com', 'telefones': '(11) 91234-5678'})
db.clientes.insertOne({'cpf': '456.789.123-45', 'nome': 'Pedro Souza', 'endereco': 'Rua João Pessoa', 'cep': '78901-234', 'email': 'pedro.souza@email.com', 'telefones': '(21) 99123-4567'})
db.clientes.insertOne({'cpf': '321.654.987-12', 'nome': 'Mariana Lima', 'endereco': 'Rua das Acácias', 'cep': '23456-789', 'email': 'mariana.lima@email.com', 'telefones': '(21) 98876-5432'})
db.clientes.insertOne({'cpf': '654.987.321-00', 'nome': 'Lucas Almeida', 'endereco': 'Rua 15 de Novembro', 'cep': '34567-890', 'email': 'lucas.almeida@email.com', 'telefones': '(31) 99111-2233'})
db.clientes.insertOne({'cpf': '213.546.879-11', 'nome': 'Fernanda Oliveira', 'endereco': 'Av. Brasil', 'cep': '98765-432', 'email': 'fernanda.oliveira@email.com', 'telefones': '(31) 99887-4455'})
db.clientes.insertOne({'cpf': '543.216.987-32', 'nome': 'Carlos Pereira', 'endereco': 'Rua do Sol', 'cep': '65432-123', 'email': 'carlos.pereira@email.com', 'telefones': '(41) 99333-2244'})
db.clientes.insertOne({'cpf': '876.543.210-65', 'nome': 'Julia Martins', 'endereco': 'Rua da Paz', 'cep': '12345-678', 'email': 'julia.martins@email.com', 'telefones': '(41) 98877-5566'})
db.clientes.insertOne({'cpf': '234.567.891-23', 'nome': 'Roberto Costa', 'endereco': 'Rua Rio Branco', 'cep': '87654-321', 'email': 'roberto.costa@email.com', 'telefones': '(51) 99222-3344'})
db.clientes.insertOne({'cpf': '678.901.234-56', 'nome': 'Renata Santos', 'endereco': 'Av. Ipiranga', 'cep': '56789-012', 'email': 'renata.santos@email.com', 'telefones': '(51) 99666-7788'})
db.produtos.insertOne({'codigo': 'N31', 'nome': 'Air Max 90', 'modelo': 'Air Max', 'fabricante': 'Nike', 'cor': '[Preto, Branco, Vermelho, Verde]', 'tam': '[38,40,41,42]'})
db.produtos.insertOne({'codigo': 'A02', 'nome': 'UltraBoost', 'modelo': 'UltraBoost', 'fabricante': 'Adidas', 'cor': '[Azul, Branco,]', 'tam': '[40,42]'})
db.produtos.insertOne({'codigo': 'N13', 'nome': 'Free Run 5.0', 'modelo': 'Free', 'fabricante': 'Nike', 'cor': '[Amarelo, Bege]', 'tam': '[39,40,42,45]'})
db.produtos.insertOne({'codigo': 'P84', 'nome': 'RS-X3', 'modelo': 'RS-X', 'fabricante': 'Puma', 'cor': '[Preto, Branco]', 'tam': '[40]'})
db.produtos.insertOne({'codigo': 'N00', 'nome': 'React Infinity Run', 'modelo': 'React', 'fabricante': 'Nike', 'cor': '[Cinza, Verde]', 'tam': '[42,43,45]'})
db.produtos.insertOne({'codigo': 'N06', 'nome': 'Zoom Freak 1', 'modelo': 'Zoom Freak', 'fabricante': 'Nike', 'cor': '[Preto]', 'tam': '[39,40,41,42]'})
db.produtos.insertOne({'codigo': 'M17', 'nome': 'Wave Rider 24', 'modelo': 'Wave Rider', 'fabricante': 'Mizuno', 'cor': '[Roxo, Verde, Rosa]', 'tam': '[38,41,42]'})
db.produtos.insertOne({'codigo': 'P08', 'nome': 'Suede Classic', 'modelo': 'Suede', 'fabricante': 'Puma', 'cor': '[Vermelho, Verde, Dourado]', 'tam': '[39,42]'})
db.produtos.insertOne({'codigo': 'A09', 'nome': 'Primeknit"', 'modelo': 'Primeknit', 'fabricante': 'Adidas', 'cor': '[Preto, Branco]', 'tam': '[39,40,41,42]'})
db.produtos.insertOne({'codigo': 'C10', 'nome': 'Chuck Taylor"', 'modelo': 'Chuck Taylor', 'fabricante': 'Converse', 'cor': '[Branco, Vermelho, Verde]', 'tam': '[39,40,41,42,43,44]'})
db.pedidos.insertOne({'id_cliente': 1, 'cliente': 'João Silva', 'endereco': 'Rua das Palmeiras', 'cep': '12345-678', 'itens': 'Tênis Nike Air Max', 'qtdes': 1, 'valor_pago': 450.0})
db.pedidos.insertOne({'id_cliente': 2, 'cliente': 'Ana Costa', 'endereco': 'Avenida Paulista', 'cep': '45678-910', 'itens': 'Tênis Adidas UltraBoost', 'qtdes': 2, 'valor_pago': 889.99})
db.pedidos.insertOne({'id_cliente': 3, 'cliente': 'Pedro Souza', 'endereco': 'Rua João Pessoa', 'cep': '78901-234', 'itens': 'Tênis Puma RS-X3', 'qtdes': 1, 'valor_pago': 350.0})
db.pedidos.insertOne({'id_cliente': 4, 'cliente': 'Mariana Lima', 'endereco': 'Rua das Acácias', 'cep': '23456-789', 'itens': 'Tênis Nike React Infinity', 'qtdes': 3, 'valor_pago': 320.0})
db.pedidos.insertOne({'id_cliente': 5, 'cliente': 'Lucas Almeida', 'endereco': 'Rua 15 de Novembro', 'cep': '34567-890', 'itens': 'Tênis Mizuno Wave Rider 24', 'qtdes': 2, 'valor_pago': 550.63})
db.pedidos.insertOne({'id_cliente': 7, 'cliente': 'Carlos Pereira', 'endereco': 'Rua do Sol', 'cep': '65432-123', 'itens': 'Tênis Converse Chuck Taylor', 'qtdes': 1, 'valor_pago': 250.2})
db.pedidos.insertOne({'id_cliente': 8, 'cliente': 'Julia Martins', 'endereco': 'Rua da Paz', 'cep': '12345-678', 'itens': 'Tênis Nike Zoom Freak', 'qtdes': 2, 'valor_pago': 900.0})
db.pedidos.insertOne({'id_cliente': 6, 'cliente': 'Fernanda Oliveira', 'endereco': 'Av. Brasil', 'cep': '98765-432', 'itens': 'Tênis Adidas EQT Support', 'qtdes': 1, 'valor_pago': 470.5})
db.pedidos.insertOne({'id_cliente': 10, 'cliente': 'Renata Santos', 'endereco': 'Av. Ipiranga', 'cep': '56789-012', 'itens': 'Tênis Reebok Speed 600', 'qtdes': 1, 'valor_pago': 120.0})
db.pedidos.insertOne({'id_cliente': 7, 'cliente': 'Carlos Pereira', 'endereco': 'Rua do Sol', 'cep': '65432-123', 'itens': 'Tênis New Balance Fresh Foam', 'qtdes': 1, 'valor_pago': 700.0})

```

### 3. Cassandra (use cqlsh)

```bash
CREATE KEYSPACE IF NOT EXISTS ecommerce
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};

USE ecommerce;
CREATE TABLE IF NOT EXISTS clientes (
    id int PRIMARY KEY,
    cpf text,
    nome text,
    endereco text,
    cep text,
    email text,
    telefone text
);
CREATE TABLE IF NOT EXISTS produtos (
    id int PRIMARY KEY,
    codigo text,
    nome text,
    modelo text,
    fabricante text,
    cor text,
    tam text
);
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
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (1, '123.456.789-01', 'João Silva', 'Rua das Palmeiras', '12345-678', 'joao.silva@email.com', '(11) 98765-4321');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (2, '987.654.321-00', 'Ana Costa', 'Avenida Paulista', '45678-910', 'ana.costa@email.com', '(11) 91234-5678');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (3, '456.789.123-45', 'Pedro Souza', 'Rua João Pessoa', '78901-234', 'pedro.souza@email.com', '(21) 99123-4567');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (4, '321.654.987-12', 'Mariana Lima', 'Rua das Acácias', '23456-789', 'mariana.lima@email.com', '(21) 98876-5432');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (5, '654.987.321-00', 'Lucas Almeida', 'Rua 15 de Novembro', '34567-890', 'lucas.almeida@email.com', '(31) 99111-2233');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (6, '213.546.879-11', 'Fernanda Oliveira', 'Av. Brasil', '98765-432', 'fernanda.oliveira@email.com', '(31) 99887-4455');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (7, '543.216.987-32', 'Carlos Pereira', 'Rua do Sol', '65432-123', 'carlos.pereira@email.com', '(41) 99333-2244');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (8, '876.543.210-65', 'Julia Martins', 'Rua da Paz', '12345-678', 'julia.martins@email.com', '(41) 98877-5566');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (9, '234.567.891-23', 'Roberto Costa', 'Rua Rio Branco', '87654-321', 'roberto.costa@email.com', '(51) 99222-3344');
INSERT INTO clientes (id, cpf, nome, endereco, cep, email, telefone) VALUES (10, '678.901.234-56', 'Renata Santos', 'Av. Ipiranga', '56789-012', 'renata.santos@email.com', '(51) 99666-7788');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (1, 'N31', 'Air Max 90', 'Air Max', 'Nike', '[Preto, Branco, Vermelho, Verde]', '[38,40,41,42]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (2, 'A02', 'UltraBoost', 'UltraBoost', 'Adidas', '[Azul, Branco,]', '[40,42]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (3, 'N13', 'Free Run 5.0', 'Free', 'Nike', '[Amarelo, Bege]', '[39,40,42,45]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (4, 'P84', 'RS-X3', 'RS-X', 'Puma', '[Preto, Branco]', '[40]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (5, 'N00', 'React Infinity Run', 'React', 'Nike', '[Cinza, Verde]', '[42,43,45]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (6, 'N06', 'Zoom Freak 1', 'Zoom Freak', 'Nike', '[Preto]', '[39,40,41,42]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (7, 'M17', 'Wave Rider 24', 'Wave Rider', 'Mizuno', '[Roxo, Verde, Rosa]', '[38,41,42]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (8, 'P08', 'Suede Classic', 'Suede', 'Puma', '[Vermelho, Verde, Dourado]', '[39,42]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (9, 'A09', 'Primeknit"', 'Primeknit', 'Adidas', '[Preto, Branco]', '[39,40,41,42]');
INSERT INTO produtos (id, codigo, nome, modelo, fabricante, cor, tam) VALUES (10, 'C10', 'Chuck Taylor"', 'Chuck Taylor', 'Converse', '[Branco, Vermelho, Verde]', '[39,40,41,42,43,44]');
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (1, 1, 'João Silva', 'Rua das Palmeiras', '12345-678', 'Tênis Nike Air Max', 1, 450.0);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (2, 2, 'Ana Costa', 'Avenida Paulista', '45678-910', 'Tênis Adidas UltraBoost', 2, 889.99);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (3, 3, 'Pedro Souza', 'Rua João Pessoa', '78901-234', 'Tênis Puma RS-X3', 1, 350.0);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (4, 4, 'Mariana Lima', 'Rua das Acácias', '23456-789', 'Tênis Nike React Infinity', 3, 320.0);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (5, 5, 'Lucas Almeida', 'Rua 15 de Novembro', '34567-890', 'Tênis Mizuno Wave Rider 24', 2, 550.63);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (6, 7, 'Carlos Pereira', 'Rua do Sol', '65432-123', 'Tênis Converse Chuck Taylor', 1, 250.2);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (7, 8, 'Julia Martins', 'Rua da Paz', '12345-678', 'Tênis Nike Zoom Freak', 2, 900.0);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (8, 6, 'Fernanda Oliveira', 'Av. Brasil', '98765-432', 'Tênis Adidas EQT Support', 1, 470.5);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (9, 10, 'Renata Santos', 'Av. Ipiranga', '56789-012', 'Tênis Reebok Speed 600', 1, 120.0);
INSERT INTO pedidos (id, id_cliente, cliente, endereco, cep, itens, qtdes, valor_pago) VALUES (10, 7, 'Carlos Pereira', 'Rua do Sol', '65432-123', 'Tênis New Balance Fresh Foam', 1, 700.0);

```
