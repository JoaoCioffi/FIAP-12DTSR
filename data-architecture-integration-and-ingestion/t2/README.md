# Projeto: ETL de Loja de Calçados - Integração de Dados Multibanco

## Disciplina: Data Architecture, Integration and Ingestion

Este projeto consiste na modelagem e integração de dados para um sistema de vendas de calçados, utilizando três tecnologias de banco de dados: **MySQL**, **Cassandra** e **MongoDB**.

## Estrutura do Projeto

```bash
.                                  # (root)
├── README.md                      # este arquivo
├── data                           # base de dados / arquivo brutos (.csv)
│   ├── clientes_concorrente.csv   # base de dados importada do concorrente (clientes - .csv - parte 03)
│   ├── cliente.csv                # base de dados inicial (clientes - .csv - partes 01, 02)
│   ├── pedidos.csv                # base de dados inicial (pedidos - .csv - partes 01, 02)
│   ├── produtos_concorrente.csv   # base de dados importada do concorrente (pedidos - .csv - parte 03)
│   └── produtos.csv               # base de dados inicial (produtos - .csv - partes 01, 02)
├── docker-compose.yaml            # arquivo yaml para buildar e instanciar as imagens (docker containers)
├── etl.py                         # script que lê cada um dos arquivos (.csv), e carrega em cada uma das bases (processo ETL)
├── handlers.py                    # script que contém os métodos próprios/wrappers de cada banco
├── queries.py                     # script que contém as query strings (puras) de cada banco (DDL/DML)
└── requirements.txt               # requisitos/libs/dependências para rodar o projeto via ETL no python
```

## Configuração de Ambiente

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

## Parte 1: Modelagem e Criação de Tabelas

O projeto define três entidades principais:

- **Produtos**
- **Clientes**
- **Pedidos**

Para cada uma dessas entidades/tabelas, temos
