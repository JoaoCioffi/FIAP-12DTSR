# Projeto: ETL de Loja de Calçados - Integração de Dados Multibanco 💡

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
  - ter Python previamente instalado (e.g Python 3.11.9) => https://www.python.org/downloads/
  - ter pip previamente instalado (e.g pip 25.1.1) => https://pypi.org/project/pip/
  - ter Docker previamente instalado (e.g Docker version 28.1.1) => https://www.docker.com
- Instalar dependências pip (package installer for Python):
  - abra o terminal na root deste projeto e rode: `pip3 install -r ./requirements.txt`
- Variáveis de ambiente:
  - as variáveis de ambiente estão no arquivo `.env.example`. Elas estão comentadas quando deve-se ou não ser definidas pelo usuário (ou por quem irá rodar o projeto). Atente-se a isso!
  - para defini-las, crie um novo arquivo no mesmo nível de disco em que está o arquivo anterior, porém nomeando-o para `.env` apenas
  - copie todo o conteúdo de `.env.example` para dentro de `.env` e altere os campos necessários.
  - variáveis como por exemplo `your_db_name_here` significam que você mesmo pode atribuir um valor que achar válido (arbitrário)

**OBS: Troubleshooting** $\rightarrow$ se mesmo após instaladas as dependências python, alguma delas não funcionar adequadamente ou ainda o script principal (etl.py) não reconhecer, vá até o script `install_requirements.ipynb` e execute ele através do environment global do jupyter (apontado para o pip global) e rode a primeira célula. É esperado que a partir daí o script principal do ETL passe a puxar as libs corretamente. Em último caso, fechar e abrir o terminal/VSCode ou até reiniciar a máquina poderá auxiliar. Não é esperado que isso ocorra, mas pode ser uma alternativa válida.

## Executando o projeto (ETL) ⌛

Para rodar o projeto, abra um terminal na root e digite `python3 .\etl.py`. O script terá uma instrução com uma observação. Atente-se a isso! Caso a entrada for inválida, a execução do script será terminada automaticamente. Esta instrução basicamente dá a escolha para o usuário sobre interromper os containers ou deixá-los ativos após o encerramento do processo ETL.

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
