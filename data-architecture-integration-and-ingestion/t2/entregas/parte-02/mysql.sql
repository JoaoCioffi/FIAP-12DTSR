-- Tabela Produtos
INSERT INTO Produtos (produto_id, codigo, nome, modelo, fabricante, cores, tamanhos) VALUES
(1, 'SH001', 'Tênis Modelo 1', 'M1', 'MarcaX', '["Preto", "Branco"]', '[38, 39, 40]'),
(2, 'SH002', 'Tênis Modelo 2', 'M2', 'MarcaX', '["Preto", "Branco"]', '[38, 39, 40]'),
(3, 'SH003', 'Tênis Modelo 3', 'M3', 'MarcaX', '["Preto", "Branco"]', '[38, 39, 40]'),
(4, 'SH004', 'Tênis Modelo 4', 'M4', 'MarcaX', '["Preto", "Branco"]', '[38, 39, 40]'),
(5, 'SH005', 'Tênis Modelo 5', 'M5', 'MarcaX', '["Preto", "Branco"]', '[38, 39, 40]');

-- Tabela Clientes
INSERT INTO Clientes (cliente_id, cpf, nome, endereco, cep, email, telefones) VALUES
(1, '1', 'Cliente 1', 'Rua 1', '12345-101', 'cliente1@email.com', '["1190000001", "112345671"]'),
(2, '2', 'Cliente 2', 'Rua 2', '12345-102', 'cliente2@email.com', '["1190000002", "112345672"]'),
(3, '3', 'Cliente 3', 'Rua 3', '12345-103', 'cliente3@email.com', '["1190000003", "112345673"]'),
(4, '4', 'Cliente 4', 'Rua 4', '12345-104', 'cliente4@email.com', '["1190000004", "112345674"]'),
(5, '5', 'Cliente 5', 'Rua 5', '12345-105', 'cliente5@email.com', '["1190000005", "112345675"]');

-- Tabela Pedidos
INSERT INTO Pedidos (pedido_id, cliente_id, endereco_entrega, cep_entrega, itens, quantidades, valor_pago) VALUES
(1, 1, 'Entrega Rua 1', '12345-201', '[101, 102]', '[1, 2]', 209.9),
(2, 2, 'Entrega Rua 2', '12345-202', '[102, 103]', '[1, 2]', 219.9),
(3, 3, 'Entrega Rua 3', '12345-203', '[103, 104]', '[1, 2]', 229.9),
(4, 4, 'Entrega Rua 4', '12345-204', '[104, 105]', '[1, 2]', 239.9),
(5, 5, 'Entrega Rua 5', '12345-205', '[105, 106]', '[1, 2]', 249.9);