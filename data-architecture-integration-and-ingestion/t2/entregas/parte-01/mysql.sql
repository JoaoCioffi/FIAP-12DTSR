-- Create Database/Schema Statement
CREATE DATABASE IF NOT EXISTS shoes_world;

-- Create Tables
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