-- PARTE 1: CRIAÇÃO DO BANCO DE DADOS E TABELAS
DROP DATABASE IF EXISTS db_vinhas_de_ouro;
-- Cria o banco de dados se ele não existir e o seleciona para uso
CREATE DATABASE IF NOT EXISTS db_vinhas_de_ouro;
USE db_vinhas_de_ouro;

-- 1. TABELA DE CATEGORIAS
-- Armazena os tipos de vinhos (Tinto, Branco, Rosé, etc.)
CREATE TABLE IF NOT EXISTS tb_categorias (
    id_categoria INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id_categoria)
);

-- 2. TABELA DE PRODUTOS
-- Armazena os detalhes de cada vinho, incluindo sua categoria
-- REMOVIDA: url_imagem desta tabela
CREATE TABLE IF NOT EXISTS tb_produtos (
    id_produto INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    descricao TEXT,
    id_categoria INT,
    PRIMARY KEY (id_produto),
    FOREIGN KEY (id_categoria) REFERENCES tb_categorias(id_categoria)
);

-- 3. TABELA DE USUÁRIOS
-- Informações dos clientes
CREATE TABLE IF NOT EXISTS tb_usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL, -- Em um sistema real, armazene senhas HASHEADAS!
    telefone VARCHAR(20),
    email VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id_usuario)
);

-- 4. TABELA DE IMAGENS
-- AGORA ESSA TABELA É A PRINCIPAL PARA AS IMAGENS DOS PRODUTOS
CREATE TABLE IF NOT EXISTS tb_imagens (
    id_imagem INT NOT NULL AUTO_INCREMENT,
    id_produto INT NOT NULL,
    url VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_imagem),
    FOREIGN KEY (id_produto) REFERENCES tb_produtos (id_produto) ON DELETE CASCADE
);

-- 5. TABELA DE COMENTÁRIOS
-- Comentários dos usuários sobre os vinhos
CREATE TABLE IF NOT EXISTS tb_comentarios (
    id_comentario INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_produto INT NOT NULL,
    comentario TEXT NOT NULL,
    PRIMARY KEY (id_comentario),
    FOREIGN KEY (id_usuario) REFERENCES tb_usuarios (id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES tb_produtos (id_produto) ON DELETE CASCADE
);

ALTER TABLE tb_comentarios
ADD COLUMN data_comentario DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- 6. TABELA DE ENDEREÇOS
-- Endereços dos usuários para entrega
CREATE TABLE IF NOT EXISTS tb_enderecos (
    id_endereco INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    cep VARCHAR(10),
    rua VARCHAR(100) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    bairro VARCHAR(100),
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_endereco),
    FOREIGN KEY (id_usuario) REFERENCES tb_usuarios (id_usuario) ON DELETE CASCADE
);

-- 7. TABELA DE ITENS DO CARRINHO
-- Armazena os produtos que um usuário adicionou ao seu carrinho de compras
CREATE TABLE IF NOT EXISTS tb_itens_carrinho (
    id_item_carrinho INT NOT NULL AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_item_carrinho),
    FOREIGN KEY (id_usuario) REFERENCES tb_usuarios (id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES tb_produtos (id_produto) ON DELETE CASCADE
);

-- PARTE 2: POPULAÇÃO INICIAL DE DADOS

-- DADOS DE CATEGORIAS
-- ID 1: Tinto
-- ID 2: Branco
-- ID 3: Rosé
-- ID 4: Espumante
-- ID 5: Sobremesa
-- ID 6: Orgânico
-- ID 7: Biodinâmico
-- ID 8: Fortificado
-- ID 9: Reserva
-- ID 10: Grand Reserva
INSERT INTO tb_categorias (nome) VALUES
('Tinto'), ('Branco'), ('Rosé'), ('Espumante'), ('Sobremesa'),
('Orgânico'), ('Biodinâmico'), ('Fortificado'), ('Reserva'), ('Grand Reserva');

-- DADOS DE USUÁRIOS
INSERT INTO tb_usuarios (usuario, senha, telefone, email) VALUES
('amelia.vinhas', 'hashed_senha_amelia', '11991112222', 'amelia.v@email.com'),
('bernardo.gomes', 'hashed_senha_bernardo', '21982223333', 'bernardo.g@email.com'),
('cecilia.costa', 'hashed_senha_cecilia', '31973334444', 'cecilia.c@email.com'),
('daniel.azevedo', 'hashed_senha_daniel', '41964445555', 'daniel.a@email.com'),
('elisa.ferreira', 'hashed_senha_elisa', '51955556666', 'elisa.f@email.com');


-- DADOS DE PRODUTOS (SEM url_imagem aqui, será na tb_imagens)
-- Vamos inserir os produtos primeiro para obter os IDs, depois inserir as imagens.

INSERT INTO tb_produtos (nome, preco, descricao, id_categoria) VALUES
-- Vinhos que você já tinha, redistribuídos:
('Vinho Tinto Cabernet Sauvignon Reserva', 125.90, 'Cabernet Sauvignon encorpado da safra 2018...', 9), -- Categoria Reserva
('Vinho Branco Sauvignon Blanc Seco', 78.00, 'Sauvignon Blanc de 2022...', 2), -- Categoria Branco
('Vinho Rosé Provence Classic', 95.50, 'Rosé delicado da região de Provence...', 3), -- Categoria Rosé
('Espumante Brut Chardonnay Nacional', 89.90, 'Espumante brut com uvas Chardonnay...', 4), -- Categoria Espumante
('Vinho do Porto Tawny 10 Anos', 180.00, 'Vinho do Porto envelhecido...', 8), -- Categoria Fortificado
('Vinho Tinto Malbec Orgânico', 65.00, 'Malbec orgânico de 2021...', 6), -- Categoria Orgânico
('Vinho Branco Riesling Doce Colheita Tardia', 110.00, 'Riesling com doçura natural...', 5), -- Categoria Sobremesa
('Vinho Tinto Pinot Noir Leve', 99.00, 'Pinot Noir leve de 2020...', 1), -- Categoria Tinto

-- Novos 30 Vinhos Icônicos e de Altíssimo Valor, com categorias atribuídas:
-- BORDEAUX (Tinto - id_categoria = 1) e alguns com 'Grand Reserva' ou 'Reserva'
('Château Pétrus Pomerol 1990', 250000.00, 'Um dos mais lendários vinhos de Bordeaux, este Pomerol à base de Merlot da safra 1990 é sinônimo de luxo e perfeição. Notas complexas de trufas, terra úmida, ameixa e especiarias, com taninos sedosos e um final interminável. Um ícone de colecionador.', 10), -- Grand Reserva
('Château Lafite Rothschild Pauillac 1982', 180000.00, 'Considerado um dos vinhos do século, esta safra do Premier Grand Cru Classé de Pauillac é sublime. Aromas de cedro, cassis e tabaco, com estrutura impecável e elegância rara. Extremamente raro e procurado.', 10), -- Grand Reserva
('Château Margaux Margaux 1996', 150000.00, 'Um dos vinhos mais femininos e perfumados de Bordeaux, o Margaux 1996 é uma obra-prima de equilíbrio e refinamento. Notas florais, de frutas vermelhas e toques minerais, com taninos finos e um frescor notável.', 1), -- Tinto
('Château Latour Pauillac 1978', 130000.00, 'Representa a força e a longevidade. O Latour 1978 é robusto, com grande concentração e capacidade de envelhecimento. Sabores de cassis, grafite e especiarias, com uma estrutura imponente que promete décadas de evolução.', 1), -- Tinto
('Château Mouton Rothschild Pauillac 1945', 500000.00, 'Uma safra histórica, este Mouton Rothschild é uma lenda viva. Intenso, com notas de chocolate, café e frutas escuras. Representa a vitória da Segunda Guerra Mundial e é um dos vinhos mais caros já leiloados.', 10), -- Grand Reserva

-- BORGONHA (Tinto - id_categoria = 1) e Grand Reserva
('Domaine de la Romanée-Conti Romanée-Conti Grand Cru 1999', 750000.00, 'O ápice da Pinot Noir na Borgonha. Este vinho é de uma complexidade e elegância incomparáveis, com camadas de frutas vermelhas, especiarias e toques terrosos. A Romanée-Conti é o Grand Cru mais prestigioso e raro do mundo.', 10), -- Grand Reserva
('Domaine Leroy Musigny Grand Cru 1990', 400000.00, 'Conhecido por sua intensidade e pureza, o Musigny da Madame Leroy é uma expressão máxima do terroir. Aromas de framboesa, cereja e violeta, com uma textura aveludada e um final etéreo. Uma joia rara da Borgonha.', 10), -- Grand Reserva
('Domaine Armand Rousseau Chambertin Grand Cru 2005', 200000.00, 'Este Chambertin é um vinho de imenso poder e elegância, refletindo a essência de um dos melhores terroirs da Borgonha. Notas de frutas silvestres, alcaçuz e minerais, com grande estrutura e profundidade.', 10), -- Grand Reserva

-- ITÁLIA (Tinto - id_categoria = 1), alguns como Reserva ou Grand Reserva
('Giacomo Conterno Monfortino Barolo Riserva 2004', 80000.00, 'Um Barolo lendário, produzido apenas nas melhores safras. Este Monfortino é um vinho de meditação, com aromas de rosa, alcatrão, cereja e especiarias. Taninos firmes e grande capacidade de envelhecimento.', 10), -- Grand Reserva
('Tenuta San Guido Sassicaia Bolgheri Sassicaia 1985', 100000.00, 'O Supertoscano original e um dos maiores vinhos da Itália. O Sassicaia 1985 é uma safra icônica, exibindo elegância e poder, com notas de cassis, cedro e menta. Um marco da vinicultura italiana.', 9), -- Reserva

-- CHAMPAGNE (Espumante - id_categoria = 4)
('Dom Pérignon P3 Plénitude Brut 1971', 120000.00, 'Uma expressão rara de Dom Pérignon, envelhecida por décadas nas caves para atingir sua "Terceira Plenitude". Aromas de frutas secas, mel e especiarias, com uma complexidade e profundidade sem igual.', 4), -- Espumante
('Louis Roederer Cristal Brut Millésimé 2002', 30000.00, 'Um Champagne de prestígio, conhecido por sua pureza e finesse. O Cristal 2002 é vibrante e elegante, com notas cítricas, de brioche e avelãs, e uma perlage finíssima e persistente.', 4), -- Espumante

-- VALLE DEL RHÔNE (Tinto - id_categoria = 1)
('E. Guigal La Mouline Côte-Rôtie 1985', 90000.00, 'Um dos "La Las" de Guigal, este Côte-Rôtie é um blend de Syrah e Viognier que atinge a perfeição. Aromas florais, de defumado, especiarias e frutas negras. Um vinho de imensa complexidade e longevidade.', 1), -- Tinto

-- Áustria (Branco - id_categoria = 2)
('F.X. Pichler "Kellerberg" Smaragd Riesling 2006', 25000.00, 'Um dos maiores Rieslings secos do mundo. Este vinho austríaco do Wachau é incrivelmente complexo, com notas de pêssego, damasco e um caráter mineral intenso. Acidez vibrante e um final extraordinariamente longo.', 2), -- Branco

-- Alemanha (Branco - id_categoria = 2) e Sobremesa
('Egon Müller Scharzhofberger Riesling Trockenbeerenauslese 2003', 600000.00, 'Considerado um dos vinhos brancos mais caros e raros do planeta. Este vinho de sobremesa alemão é um néctar concentrado, com notas de mel, frutas exóticas e uma acidez que equilibra perfeitamente a doçura. Produção minúscula.', 5), -- Sobremesa

-- FORTIFICADOS / SOBREMESA (id_categoria = 5 ou 8)
('W&J Graham’s Vintage Port 1970', 10000.00, 'Um dos mais celebrados Vinhos do Porto Vintage. O Graham’s 1970 é denso e complexo, com aromas de frutas escuras, chocolate e especiarias, e uma capacidade de envelhecimento que se estende por décadas.', 8), -- Fortificado
('Château d’Yquem Sauternes 1988', 35000.00, 'O mais famoso vinho de sobremesa do mundo. Este Sauternes de Bordeaux é dourado e luxuoso, com aromas de mel, damasco seco, casca de laranja e especiarias. Doçura e acidez perfeitamente equilibradas.', 5), -- Sobremesa

-- CALIFÓRNIA (Tinto - id_categoria = 1) e Grand Reserva
('Screaming Eagle Cabernet Sauvignon Napa Valley 1992', 500000.00, 'Um "cult wine" da Califórnia, conhecido por sua exclusividade e alta demanda. Este Cabernet Sauvignon é potente e elegante, com notas de cassis, tabaco e cedro, e um final incrivelmente longo. Produção limitadíssima.', 10), -- Grand Reserva
('Harlan Estate Napa Valley 1994', 100000.00, 'Outro gigante da Califórnia, o Harlan Estate é um blend de Bordeaux que representa o auge da vinicultura no Novo Mundo. Complexo, com camadas de frutas, terra e especiarias, e uma estrutura monumental.', 10), -- Grand Reserva

-- Espanha (Tinto - id_categoria = 1) e Grand Reserva
('Vega Sicilia Único Ribera del Duero 1962', 45000.00, 'Um clássico espanhol, o Único é um vinho de longevidade lendária. Esta safra rara oferece aromas complexos de frutas secas, couro, tabaco e especiarias. Elegante e com grande profundidade.', 10), -- Grand Reserva

-- Húngria (Sobremesa - id_categoria = 5)
('Royal Tokaji Essencia 2000', 70000.00, 'O Tokaji Essencia é um dos vinhos mais concentrados e raros do mundo, feito a partir da primeira lágrima das uvas botrytizadas. Néctar de mel, damasco e laranja, com uma acidez vibrante que o torna imortal.', 5), -- Sobremesa

-- Vinhos raros adicionais, com categorias atribuídas:
('Penfolds Grange Shiraz 1951', 300000.00, 'Um vinho icônico da Austrália, conhecido por sua raridade e extrema longevidade. O Grange 1951 é o primeiro de sua espécie, com aromas intensos e complexos de especiarias e frutas escuras. Uma peça de museu.', 10), -- Grand Reserva
('DRC La Tâche Grand Cru 2005', 300000.00, 'Um dos mais finos vinhos da Borgonha, conhecido por sua incrível finesse e complexidade. Aromas de especiarias, frutas vermelhas e notas terrosas, com uma textura etérea e final persistente.', 10), -- Grand Reserva
('Henri Jayer Cros Parantoux Vosne-Romanée 1990', 800000.00, 'Um dos vinhos mais lendários e procurados do mundo, vindo de uma pequena e excepcional parcela na Borgonha, vinificado pelo lendário Henri Jayer. Extremamente raro e valorizado por colecionadores.', 10), -- Grand Reserva
('Petrus Pomerol 2000', 300000.00, 'Outra safra lendária de Pétrus, este Pomerol do ano 2000 é poderoso e sedutor. Taninos finos, aromas de trufas negras, ameixa e toques de cacau. Um vinho de grande profundidade e que pode envelhecer por décadas.', 10), -- Grand Reserva
('Domaine de la Romanée-Conti Montrachet Grand Cru 2009', 250000.00, 'O mais prestigioso vinho branco da Borgonha. Este Montrachet é um Chardonnay de rara complexidade, com notas de avelhã, mel e cítricos, e uma mineralidade impressionante. De produção minúscula e altíssima demanda.', 2), -- Branco
('Château Cheval Blanc Saint-Émilion Grand Cru Classé (A) 1947', 600000.00, 'Uma safra mítica de um dos maiores vinhos de Saint-Émilion. Este blend de Cabernet Franc e Merlot é conhecido por sua opulência, riqueza e complexidade aromática, com notas de couro e frutas cozidas. Um vinho de lenda.', 10), -- Grand Reserva
('Screaming Eagle Sauvignon Blanc Napa Valley 2010', 80000.00, 'O Sauvignon Blanc mais exclusivo e raro da Califórnia. Com produção minúscula, este vinho branco de culto oferece frescor, mineralidade e complexidade, com notas de frutas cítricas e toques herbáceos.', 2), -- Branco
('Salon Le Mesnil Blanc de Blancs Brut 1996', 70000.00, 'Um Champagne ultra-premium e exclusivo, feito apenas com uvas Chardonnay de um único vinhedo Grand Cru e apenas em safras excepcionais. Famoso por sua pureza, mineralidade e incrível longevidade.', 4), -- Espumante
('Masseto Toscana IGT 2006', 40000.00, 'O "Merlot" italiano, este Supertoscano é produzido a partir de um único vinhedo. Rico, opulento e com grande estrutura, o Masseto é um vinho de culto com aromas de frutas negras, chocolate e toques de baunilha.', 1), -- Tinto
('Concha y Toro Don Melchor Puente Alto Cabernet Sauvignon 1988', 15000.00, 'Um dos primeiros grandes Cabernets do Chile a ganhar reconhecimento internacional. Este Don Melchor representa a excelência chilena, com notas de cassis, cedro e especiarias, e uma estrutura elegante.', 9), -- Reserva
('Colgin IX Estate Napa Valley 2007', 30000.00, 'Um dos "cult wines" mais prestigiados de Napa Valley. Este blend bordalês exibe riqueza, complexidade e equilíbrio, com taninos finos e um final longo. Produção artesanal e muito limitada.', 1); -- Tinto


-- DADOS DE IMAGENS
-- AGORA AS IMAGENS SÃO INSERIDAS AQUI, REFERENCIANDO O id_produto
-- IMPORTANTE: Os IDs dos produtos (id_produto) serão gerados automaticamente
-- pela sequência dos INSERTs acima. O primeiro produto terá id_produto = 1, o segundo = 2, etc.
-- Certifique-se de que a ordem dos INSERTs de produtos e imagens corresponda.

INSERT INTO tb_imagens (id_produto, url) VALUES
-- Vinhos que você já tinha: (id_produto 1 ao 8) com duplicação
(1, 'https://t75868.vteximg.com.br/arquivos/ids/156740/Reserva-Cabernet-Sauvignon.png?v=638042246966170000'),
(1, 'https://t75868.vteximg.com.br/arquivos/ids/156740/Reserva-Cabernet-Sauvignon.png?v=638042246966170000'),
(2, 'https://cdn.dooca.store/278/products/04vcmuht76dbxf8okprevf1nypcs8jea92h4_600x800+fill_ffffff.jpg?v=1728071669'),
(2, 'https://cdn.dooca.store/278/products/04vcmuht76dbxf8okprevf1nypcs8jea92h4_600x800+fill_ffffff.jpg?v=1728071669'),
(3, 'https://images.vivino.com/thumbs/ZI-QLtenQP-0W73eKnbpUw_pb_x960.png'),
(3, 'https://images.vivino.com/thumbs/ZI-QLtenQP-0W73eKnbpUw_pb_x960.png'),
(4, 'https://www.vinhosevinhos.com/media/catalog/product/cache/f551083cd20de7ac8cf7d25adc91480d/g/a/garibaldi-chardonnay.jpg'),
(4, 'https://www.vinhosevinhos.com/media/catalog/product/cache/f551083cd20de7ac8cf7d25adc91480d/g/a/garibaldi-chardonnay.jpg'),
(5, 'https://cdn.mistral.com.br/products/1393/img_m_1393.png'),
(5, 'https://cdn.mistral.com.br/products/1393/img_m_1393.png'),
(6, 'https://lapastina.vtexassets.com/arquivos/ids/159703-1200-auto?v=638016208549830000&width=1200&height=auto&aspect=true'),
(6, 'https://lapastina.vtexassets.com/arquivos/ids/159703-1200-auto?v=638016208549830000&width=1200&height=auto&aspect=true'),
(7, 'https://interstore.vtexassets.com/arquivos/ids/158261-1200-auto?v=638109576890000000&width=1200&height=auto&aspect=true'),
(7, 'https://interstore.vtexassets.com/arquivos/ids/158261-1200-auto?v=638109576890000000&width=1200&height=auto&aspect=true'),
(8, 'https://t75868.vteximg.com.br/arquivos/ids/156742/Varietal-Pinot-Noir.png?v=638042249085770000'),
(8, 'https://t75868.vteximg.com.br/arquivos/ids/156742/Varietal-Pinot-Noir.png?v=638042249085770000'),

-- Novos 30 Vinhos Icônicos e de Altíssimo Valor: (id_produto 9 ao 38) com duplicação
(9, 'https://www.bancadoramon.com.br/media/catalog/product/cache/1/thumbnail/520x/9df78eab33525d08d6e5fb8d27136e95/p/e/petrus_97.jpg'),
(9, 'https://www.bancadoramon.com.br/media/catalog/product/cache/1/thumbnail/520x/9df78eab33525d08d6e5fb8d27136e95/p/e/petrus_97.jpg'),
(10, 'https://www.garrafeiranacional.com/media/catalog/product/cache/486a54b851bffbba125fcd174833233f/6/1/6191530-0.jpg'),
(10, 'https://www.garrafeiranacional.com/media/catalog/product/cache/486a54b851bffbba125fcd174833233f/6/1/6191530-0.jpg'),
(11, 'https://www.garrafeiranacional.com/media/catalog/product/cache/486a54b851bffbba125fcd174833233f/6/1/6190623-0.jpg'),
(11, 'https://www.garrafeiranacional.com/media/catalog/product/cache/486a54b851bffbba125fcd174833233f/6/1/6190623-0.jpg'),
(12, 'https://www.garrafeiranacional.com/media/catalog/product/cache/486a54b851bffbba125fcd174833233f/6/1/6190539_2_.jpg'),
(12, 'https://www.garrafeiranacional.com/media/catalog/product/cache/486a54b851bffbba125fcd174833233f/6/1/6190539_2_.jpg'),
(13, 'https://www.sodivin.com/img/p/1/4/5/8/6/14586-pdt_540.webp'),
(13, 'https://www.sodivin.com/img/p/1/4/5/8/6/14586-pdt_540.webp'),
(14, 'https://pleasurewine.com/14560-superlarge_default/romanee-conti-1999-domaine-de-la-romanee-conti.jpg'),
(14, 'https://pleasurewine.com/14560-superlarge_default/romanee-conti-1999-domaine-de-la-romanee-conti.jpg'),
(15, 'https://www.wineinvestment.com/assets/Uploads/Domaine_Leroy_-_Musigny_Grand_Cru__ScaleMaxWidthWzQwMF0.png'),
(15, 'https://www.wineinvestment.com/assets/Uploads/Domaine_Leroy_-_Musigny_Grand_Cru__ScaleMaxWidthWzQwMF0.png'),
(16, 'https://pleasurewine.com/9154-superlarge_default/chambertin-grand-cru-2005-domaine-armand-rousseau.jpg'),
(16, 'https://pleasurewine.com/9154-superlarge_default/chambertin-grand-cru-2005-domaine-armand-rousseau.jpg'),
(17, 'https://133973339.cdn6.editmysite.com/uploads/1/3/3/9/133973339/3CEAJXZBMSGNBQKBYPFBXY7L.jpeg?width=2560&optimize=medium'),
(17, 'https://133973339.cdn6.editmysite.com/uploads/1/3/3/9/133973339/3CEAJXZBMSGNBQKBYPFBXY7L.jpeg?width=2560&optimize=medium'),
(18, 'https://enotecaproperzio.gumlet.io/media/catalog/product/cache/1/image/400x600/9df78eab33525d08d6e5fb8d27136e95/s/a/b259254ee82bf571ece7e7f84305a1d6/sassicaia-tenuta-san-guido-1985-0-75-lt.png'),
(18, 'https://enotecaproperzio.gumlet.io/media/catalog/product/cache/1/image/400x600/9df78eab33525d08d6e5fb8d27136e95/s/a/b259254ee82bf571ece7e7f84305a1d6/sassicaia-tenuta-san-guido-1985-0-75-lt.png'),
(19, 'https://www.wine-searcher.com/images/labels/86/83/10708683.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(19, 'https://www.wine-searcher.com/images/labels/86/83/10708683.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(20, 'https://www.wine-searcher.com/images/labels/19/63/10141963.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(20, 'https://www.wine-searcher.com/images/labels/19/63/10141963.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(21, 'https://www.wine-searcher.com/images/labels/11/71/11741171.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(21, 'https://www.wine-searcher.com/images/labels/11/71/11741171.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(22, 'https://www.wine-searcher.com/images/labels/26/47/10522647.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(22, 'https://www.wine-searcher.com/images/labels/26/47/10522647.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(23, 'https://www.wine-searcher.com/images/labels/37/62/11593762.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(23, 'https://www.wine-searcher.com/images/labels/37/62/11593762.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(24, 'https://www.wine-searcher.com/images/labels/53/32/11765332.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(24, 'https://www.wine-searcher.com/images/labels/53/32/11765332.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(25, 'https://www.garrafeiranacional.com/media/catalog/product/cache/e37fd98e323045f31cb97da19fc50468/6/1/6190744-0.jpg'),
(25, 'https://www.garrafeiranacional.com/media/catalog/product/cache/e37fd98e323045f31cb97da19fc50468/6/1/6190744-0.jpg'),
(26, 'https://www.wine-searcher.com/images/labels/89/35/11748935.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(26, 'https://www.wine-searcher.com/images/labels/89/35/11748935.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(27, 'https://www.wine-searcher.com/images/labels/50/84/11715084.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(27, 'https://www.wine-searcher.com/images/labels/50/84/11715084.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(28, 'https://www.wine-searcher.com/images/labels/84/85/11628485.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(28, 'https://www.wine-searcher.com/images/labels/84/85/11628485.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(29, 'https://acdn-us.mitiendanube.com/stores/003/725/843/products/tokaji-86c275188018c5a9a816970154547818-1024-1024.webp'),
(29, 'https://acdn-us.mitiendanube.com/stores/003/725/843/products/tokaji-86c275188018c5a9a816970154547818-1024-1024.webp'),
(30, 'https://www.wine-searcher.com/images/labels/49/79/11824979.jpg?width=466&height=400&fit=bounds'),
(30, 'https://www.wine-searcher.com/images/labels/49/79/11824979.jpg?width=466&height=400&fit=bounds'),
(31, 'https://www.wine-searcher.com/images/labels/29/83/10112983.jpg?width=466&height=400&fit=bounds'),
(31, 'https://www.wine-searcher.com/images/labels/29/83/10112983.jpg?width=466&height=400&fit=bounds'),
(32, 'https://www.wine-searcher.com/images/labels/67/23/10436723.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(32, 'https://www.wine-searcher.com/images/labels/67/23/10436723.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(33, 'https://www.wine-searcher.com/images/labels/58/95/11705895.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(33, 'https://www.wine-searcher.com/images/labels/58/95/11705895.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(34, 'https://www.wine-searcher.com/images/labels/90/23/10399023.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(34, 'https://www.wine-searcher.com/images/labels/90/23/10399023.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(35, 'https://worldwine.vtexassets.com/arquivos/ids/167524-1200-auto?v=638485315219500000&width=1200&height=auto&aspect=true'),
(35, 'https://worldwine.vtexassets.com/arquivos/ids/167524-1200-auto?v=638485315219500000&width=1200&height=auto&aspect=true'),
(36, 'https://www.wine-searcher.com/images/labels/72/75/11667275.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(36, 'https://www.wine-searcher.com/images/labels/72/75/11667275.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(37, 'https://www.wine-searcher.com/images/labels/36/81/10513681.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(37, 'https://www.wine-searcher.com/images/labels/36/81/10513681.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(38, 'https://www.wine-searcher.com/images/labels/55/95/10155595.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(38, 'https://www.wine-searcher.com/images/labels/55/95/10155595.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(39, 'https://www.wine-searcher.com/images/labels/30/42/11713042.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(39, 'https://www.wine-searcher.com/images/labels/30/42/11713042.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(40, 'https://www.wine-searcher.com/images/labels/81/48/10408148.jpg?width=175&height=234&fit=bounds&canvas=180,240'),
(40, 'https://www.wine-searcher.com/images/labels/81/48/10408148.jpg?width=175&height=234&fit=bounds&canvas=180,240');


-- DADOS DE COMENTÁRIOS
INSERT INTO tb_comentarios (id_usuario, id_produto, comentario) VALUES
(1, 1, 'Um tinto espetacular, complexo e com final longo!'),
(2, 3, 'Rosé leve, saboroso e muito refrescante para o verão.'),
(1, 2, 'Refrescante e com uma acidez perfeita para acompanhar peixes leves.'),
(3, 1, 'Meu Cabernet favorito, com aromas de frutas negras e um toque de carvalho.'),
(2, 5, 'Um vinho do Porto delicioso e aveludado, ideal para a sobremesa.'),
(1, 6, 'Excelente custo-benefício para um Malbec orgânico, muito frutado.'),
(3, 8, 'Pinot Noir leve e elegante, combina com diversas ocasiões.'),
(4, 9, 'Pétrus 1990 é uma experiência única, inesquecível e luxuosa.'), -- Novo vinho
(5, 12, 'O Cristal 2002 é a perfeição em forma de champagne, bolhas delicadas e sabor inigualável.'), -- Novo vinho
(1, 15, 'Sauternes 1988: doçura divina com acidez equilibrada, um verdadeiro néctar!'); -- Novo vinho


-- DADOS DE ENDEREÇOS
INSERT INTO tb_enderecos (id_usuario, cep, rua, numero, bairro, cidade, estado) VALUES
(1, '01001-000', 'Rua dos Vinhedos', '123', 'Vila da Uva', 'São Paulo', 'SP'),
(1, '01002-000', 'Av. dos Produtores', '456', 'Centro', 'São Paulo', 'SP'),
(2, '20000-000', 'Rua da Adega', '789', 'Laranjeiras', 'Rio de Janeiro', 'RJ'),
(3, '30000-000', 'Alameda do Vinho', '101', 'Savassi', 'Belo Horizonte', 'MG'),
(4, '90000-000', 'Travessa dos Barris', '202', 'Floresta', 'Porto Alegre', 'RS'),
(5, '70000-000', 'Setor de Vinícolas', '303', 'Asa Norte', 'Brasília', 'DF');

-- DADOS DE ITENS DO CARRINHO (com quantidade especificada)
-- Note que os id_produto precisam ser atualizados para corresponder aos novos IDs gerados
-- Pelo script, os IDs de produto serão sequenciais a partir de 1.
-- Por exemplo, o 'Vinho Tinto Cabernet Sauvignon Reserva' terá id_produto = 1,
-- e o 'Château Pétrus Pomerol 1990' terá id_produto = 9, etc.
INSERT INTO tb_itens_carrinho (id_usuario, id_produto, quantidade) VALUES
(1, 1, 1),  -- Vinho Tinto Cabernet Sauvignon Reserva
(1, 3, 2),  -- Vinho Rosé Provence Classic
(2, 2, 1),  -- Vinho Branco Sauvignon Blanc Seco
(3, 4, 1),  -- Espumante Brut Chardonnay Nacional
(3, 8, 2),  -- Vinho Tinto Pinot Noir Leve
(4, 9, 1),  -- Château Pétrus Pomerol 1990
(5, 20, 1), -- Louis Roederer Cristal Brut Millésimé 2002
(1, 25, 1); -- Château d’Yquem Sauternes 1988