🍷 As Videiras de Ouro - Sua Adega Online Premium
Bem-vindo ao Vinhas de Ouro, seu destino online para explorar e adquirir vinhos excepcionais, desde rótulos do dia a dia até garrafas icônicas de colecionador. Nossa plataforma oferece uma experiência intuitiva para descobrir vinhos por categoria e desfrutar de descrições detalhadas.


🚀 Visão Geral
Este é um aplicativo web Flask que simula uma loja de vinhos, permitindo a visualização de produtos categorizados, detalhes de cada vinho e, futuramente, funcionalidades de carrinho de compras e gestão de usuários. A arquitetura do banco de dados é cuidadosamente projetada para gerenciar informações de produtos, categorias, usuários, endereços, comentários e imagens.


✨ Funcionalidades Atuais
Listagem de Produtos: Navegue por uma vasta seleção de vinhos.
Filtragem por Categoria: Encontre facilmente vinhos Tintos, Brancos, Rosés, Espumantes, Sobremesa, Orgânicos, Biodinâmicos, Fortificados, Reserva e Grand Reserva.
Detalhes do Produto: Visualize informações detalhadas de cada vinho, incluindo nome, preço, descrição e imagem.
Gestão de Imagens: As imagens dos produtos são armazenadas em uma tabela dedicada (tb_imagens) para flexibilidade e escalabilidade futura (ex: galerias de fotos).


🛠️ Tecnologias Utilizadas
Backend: Python 3 com Flask
Banco de Dados: MySQL
Templates: Jinja2
Conector MySQL para Python: mysql.connector (ou MySQLdb, dependendo da sua escolha)


⚙️ Configuração e Instalação
Siga estes passos para configurar e rodar o projeto em seu ambiente local.

Pré-requisitos
Certifique-se de ter instalado:

Python 3.x
MySQL Server
pip (gerenciador de pacotes do Python)



1. Configuração do Banco de Dados

Crie o Banco de Dados e Tabelas:

Acesse seu cliente MySQL (ex: MySQL Workbench, linha de comando).
Execute o script SQL fornecido (o último que inclui a realocação das imagens para tb_imagens e a reorganização dos produtos). Este script irá criar o banco de dados db_vinhas_de_ouro, todas as tabelas e popular com os dados iniciais, incluindo a atribuição correta das categorias e URLs das imagens.
SQL

-- Exemplo de como dropar e recriar o DB (use com cautela, apaga dados existentes!)
DROP DATABASE IF EXISTS db_vinhas_de_ouro;
-- COLOQUE AQUI O CONTEÚDO COMPLETO DO SCRIPT SQL MAIS RECENTE
-- (que inclui a criação do DB, tabelas, categorias, produtos e imagens em tb_imagens)
Ajuste as Credenciais do Banco de Dados:

No arquivo app_webService/data/conection.py, atualize as credenciais de acesso ao seu servidor MySQL (host, user, password, database).
Python

# app_webService/data/conection.py

class Conection:
    def __init__(self):<br>
        self.host = "localhost"<br>
        self.user = "root"<br>
        self.password = "sua_senha_do_mysql" # <-- ATUALIZE AQUI<br>
        self.database = "db_vinhas_de_ouro"<br>


2. Configuração do Ambiente Python

Clone o Repositório (se aplicável, caso seu código esteja em um Git) ou navegue até a pasta do seu projeto.

Crie um Ambiente Virtual (recomendado):

Bash

python -m venv venv
Ative o Ambiente Virtual:

Windows:
Bash

.\venv\Scripts\activate
macOS/Linux:
Bash

source venv/bin/activate
Instale as Dependências:

Bash

pip install -r requirements.txt

3. Executando a Aplicação

Certifique-se de que seu ambiente virtual esteja ativado.

A partir da raiz do seu projeto, execute o arquivo principal da aplicação:

Bash

python app.py
A aplicação estará disponível em http://127.0.0.1:5000/ (ou outra porta, se configurado).


📂 Estrutura do Projeto
your_flask_app/
├── app.py                      # Arquivo principal do Flask, rotas e inicialização
├── app_webService/             # Lógica de negócio e acesso a dados
│   ├── data/
│   │   └── conection.py        # Classe para conexão com o banco de dados
│   └── models/
│       ├── categories.py       # Modelo para operações com categorias
│       └── products.py         # Modelo para operações com produtos (ajustado para JOIN com imagens)
└── templates/
    └── index.html              # Template HTML principal para exibição dos vinhos


⚠️ Ponto de Atenção para Desenvolvimento
Com a mudança das imagens para a tabela tb_imagens, certifique-se de que as suas consultas no app_webService/models/products.py estejam utilizando um LEFT JOIN para recuperar a URL da imagem principal junto com os dados do produto. O template HTML não precisará de modificações se a coluna da URL for renomeada para url_imagem na consulta (i.url AS url_imagem).


Esperamos que você aproveite a experiência com o Vinhas de Ouro! Se tiver alguma dúvida ou precisar de mais funcionalidades, sinta-se à vontade para expandir este projeto.
