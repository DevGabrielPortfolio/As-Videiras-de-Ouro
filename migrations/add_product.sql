INSERT INTO tb_categorias (nome)
VALUES ('TESTE')
ON DUPLICATE KEY UPDATE nome = nome;

SELECT id_categoria FROM tb_categorias WHERE nome = 'TESTE';

INSERT INTO tb_produtos (nome, preco, descricao, id_categoria)
VALUES (
    'Vinho TESTE',
    100.00,
    'Descricao teste',
    11
);

SELECT LAST_INSERT_ID() AS id_produto;

INSERT INTO tb_imagens (id_produto, url)
  VALUES (41, 'https://images.tcdn.com.br/img/img_prod/463054/produto_teste_nao_comprar_2963_1_20240621144802.png');


  