from config.data.connection import Conection
from mysql.connector import Error # Importa especificamente a classe Error para tratamento de exceções

class Wines:

    @staticmethod
    def get_all_wines():
        """
        Retorna todos os vinhos com suas respectivas imagens, agrupadas.
        Utiliza um LEFT JOIN para buscar vinhos e suas imagens em uma única consulta,
        e context managers para garantir o fechamento adequado da conexão e do cursor.
        """
        wines_with_images = []
        try:
            # Usa context manager para a conexão. Garante que conn.close() será chamado.
            with Conection.create_conection() as conn:
                if conn is None:
                    print("ERRO_WINE_CONNECTION: Falha ao conectar ao banco de dados para obter todos os vinhos.")
                    return []
                
                # Usa context manager para o cursor. Garante que cursor.close() será chamado.
                with conn.cursor(dictionary=True) as cursor: # dictionary=True retorna resultados como dicionários
                    # Consulta SQL otimizada para buscar vinhos e todas as suas imagens
                    # LEFT JOIN tb_imagens garante que vinhos sem imagens também sejam incluídos.
                    # ORDER BY p.id_produto, i.id_imagem é crucial para o agrupamento em Python.
                    sql = """
                        SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                        FROM tb_produtos p
                        LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                        ORDER BY p.id_produto, i.id_imagem;
                    """
                    cursor.execute(sql)
                    
                    # ESSENCIAL: Consome todos os resultados da consulta.
                    # Isso previne o erro 'Unread result found'.
                    rows = cursor.fetchall() 

                    # Dicionário para agrupar as imagens a cada vinho
                    wines_dict = {}
                    for row in rows:
                        wine_id = row['id_produto']
                        # Se o vinho ainda não foi adicionado ao dicionário, crie sua entrada base
                        if wine_id not in wines_dict:
                            wines_dict[wine_id] = {
                                'id_produto': row['id_produto'],
                                'nome': row['nome'],
                                'preco': row['preco'],
                                'descricao': row['descricao'],
                                'imagens': [] # Inicializa uma lista vazia para as URLs das imagens
                            }
                        # Adiciona a URL da imagem à lista de imagens do vinho correspondente
                        # Garante que 'None' não seja adicionado se o vinho não tiver imagens
                        if row['imagem_url']: 
                            wines_dict[wine_id]['imagens'].append({'url': row['imagem_url']})

                    # Converte o dicionário de vinhos de volta para uma lista de dicionários
                    wines_with_images = list(wines_dict.values())
                    return wines_with_images

        except Error as e: # Captura erros específicos do MySQL Connector
            print(f"ERRO_WINE_SQL (get_all_wines): Erro no banco de dados ao obter todos os vinhos: {e}")
            return []
        except Exception as e: # Captura quaisquer outras exceções inesperadas
            print(f"ERRO_WINE_GERAL (get_all_wines): Erro inesperado ao obter todos os vinhos: {e}")
            return []
        # O bloco 'finally' com cursor.close() e conn.close() não é mais necessário
        # devido ao uso dos 'with' statements (context managers).


    @staticmethod
    def get_wines_by_category(category_id):
        """
        Retorna vinhos de uma categoria específica com suas respectivas imagens.
        Utiliza LEFT JOIN e context managers para garantir o fechamento adequado.
        """
        wines_with_images = []
        try:
            # Usa context manager para a conexão
            with Conection.create_conection() as conn:
                if conn is None:
                    print(f"ERRO_WINE_CONNECTION: Falha ao conectar ao banco de dados para obter vinhos na categoria {category_id}.")
                    return []
                
                # Usa context manager para o cursor
                with conn.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                        FROM tb_produtos p
                        LEFT JOIN tb_categorias c ON p.id_categoria = c.id_categoria
                        LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                        WHERE c.id_categoria = %s
                        ORDER BY p.id_produto, i.id_imagem;
                    """
                    cursor.execute(sql, (category_id,))
                    
                    # ESSENCIAL: Consome todos os resultados da consulta.
                    # Isso previne o erro 'Unread result found'.
                    rows = cursor.fetchall()

                    wines_dict = {}
                    for row in rows:
                        wine_id = row['id_produto']
                        if wine_id not in wines_dict:
                            wines_dict[wine_id] = {
                                'id_produto': row['id_produto'],
                                'nome': row['nome'],
                                'preco': row['preco'],
                                'descricao': row['descricao'],
                                'imagens': []
                            }
                        if row['imagem_url']:
                            wines_dict[wine_id]['imagens'].append({'url': row['imagem_url']})

                    wines_with_images = list(wines_dict.values())
                    return wines_with_images

        except Error as e:
            print(f"ERRO_WINE_SQL (get_wines_by_category): Erro no banco de dados ao obter vinhos por categoria: {e}")
            return []
        except Exception as e:
            print(f"ERRO_WINE_GERAL (get_wines_by_category): Erro inesperado ao obter vinhos por categoria: {e}")
            return []


    @staticmethod
    def get_wine_by_id(wine_id):
        """
        Retorna um único vinho pelo ID com todas as suas imagens.
        Utiliza LEFT JOIN e context managers para garantir o fechamento adequado.
        """
        try:
            # Usa context manager para a conexão
            with Conection.create_conection() as conn:
                if conn is None:
                    print("ERRO_WINE_CONNECTION: Falha ao conectar ao banco de dados para obter vinho por ID.")
                    return None
                
                # Usa context manager para o cursor
                with conn.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                        FROM tb_produtos p
                        LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                        WHERE p.id_produto = %s
                        ORDER BY i.id_imagem;
                    """
                    cursor.execute(sql, (wine_id,))
                    
                    # ESSENCIAL: Consome todos os resultados da consulta.
                    # Isso previne o erro 'Unread result found'.
                    rows = cursor.fetchall()

                    if not rows:
                        return None # Vinho não encontrado

                    # Como pode haver múltiplas linhas para o mesmo vinho (uma por imagem),
                    # pegamos os dados base do primeiro registro e agrupamos as imagens.
                    wine_data = {
                        'id_produto': rows[0]['id_produto'],
                        'nome': rows[0]['nome'],
                        'preco': rows[0]['preco'],
                        'descricao': rows[0]['descricao'],
                        'imagens': []
                    }
                    for row in rows:
                        if row['imagem_url']:
                            wine_data['imagens'].append({'url': row['imagem_url']})

                    return wine_data

        except Error as e:
            print(f"ERRO_WINE_SQL (get_wine_by_id): Erro no banco de dados ao obter vinho por ID: {e}")
            return None
        except Exception as e:
            print(f"ERRO_WINE_GERAL (get_wine_by_id): Erro inesperado ao obter vinho por ID: {e}")
            return None

