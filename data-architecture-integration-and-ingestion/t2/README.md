# Projeto: ETL de Loja de Calçados - Integração de Dados Multibanco

## 📅 Disciplina: Data Architecture, Integration and Ingestion

Este projeto consiste na modelagem e integração de dados para um sistema de vendas de calçados, utilizando três tecnologias de banco de dados: **MySQL**, **Cassandra** e **MongoDB**. Para fins deste trabalho, implementamos totalmente a solução com **MySQL**, cobrindo as três partes propostas:

---

## ✍️ Parte 1: Modelagem e Criação de Tabelas

O projeto define três entidades principais:

- **Produtos**
- **Clientes**
- **Pedidos**

O schema está centralizado no arquivo `schema.json`, que define os campos e tipos para cada entidade em formato Python (e.g. `int`, `str`, `list[str]`).

O script `etl.py` é responsável por orquestrar a criação das tabelas no MySQL utilizando a classe `MySQL` de `queries.py`, que mapeia dinamicamente os tipos para sintaxe SQL.

### 🔧 SQL Gerado para Criação das Tabelas (MySQL)

#### Produtos

```sql
CREATE TABLE IF NOT EXISTS `Produtos` (
  `produto_id` INT,
  `codigo` VARCHAR(255),
  `nome` VARCHAR(255),
  `modelo` VARCHAR(255),
  `fabricante` VARCHAR(255),
  `cores` JSON,
  `tamanhos` JSON,
  PRIMARY KEY (`produto_id`)
);
```

#### Clientes

```sql
CREATE TABLE IF NOT EXISTS `Clientes` (
  `cliente_id` INT,
  `cpf` VARCHAR(255),
  `nome` VARCHAR(255),
  `endereco` VARCHAR(255),
  `cep` VARCHAR(255),
  `email` VARCHAR(255),
  `telefones` JSON,
  PRIMARY KEY (`cliente_id`)
);
```

#### Pedidos

```sql
CREATE TABLE IF NOT EXISTS `Pedidos` (
  `pedido_id` INT,
  `cliente_id` INT,
  `endereco_entrega` VARCHAR(255),
  `cep_entrega` VARCHAR(255),
  `itens` JSON,
  `quantidades` JSON,
  `valor_pago` FLOAT,
  PRIMARY KEY (`pedido_id`)
);
```

---

## ✅ Parte 2: Inserção de Dados de Exemplo

Os arquivos CSV com dados fictícios estão localizados na pasta `data/`, contendo 10 registros por tabela:

- `clientes_sample.csv`
- `produtos_sample.csv`
- `pedidos_sample.csv`

A inserção é feita automaticamente pelo `etl.py`, utilizando `executemany` com os dados lidos via `pandas`.

### 🔧 SQL Base para Inserção (formato dinâmico):

```sql
INSERT INTO `Tabela` (`coluna1`, `coluna2`, ...) VALUES (%s, %s, ...);
```

---

## 🛎 Parte 3: Integração com Dados de Concorrente

Arquivos CSV simulando a aquisição de um concorrente foram criados:

- `clientes_concorrente.csv` (20 registros)
- `produtos_concorrente.csv` (20 registros)

O método `.update()` da classe `MySQL` reaproveita o `.insert()` para realizar a carga adicional sem conflitos, já que os IDs começam em 1001.

### 🔧 SQL Base para Atualização via Insert:

```sql
INSERT INTO `Clientes` (...) VALUES (...);
INSERT INTO `Produtos` (...) VALUES (...);
```

---

## 📂 Estrutura de Arquivos do Projeto

```bash
.
├── data/
│   ├── clientes_sample.csv
│   ├── produtos_sample.csv
│   ├── pedidos_sample.csv
│   ├── clientes_concorrente.csv
│   └── produtos_concorrente.csv
├── etl.py
├── queries.py
├── schema.json
├── .env
└── README.md
```

---

## 🌐 Tecnologias Utilizadas

- Python 3.12
- MySQL 8+
- pandas
- mysql-connector-python
- python-dotenv

---

## 🌟 Autor

João Cioffi MBA Data Science & Artificial Intelligence - FIAP
