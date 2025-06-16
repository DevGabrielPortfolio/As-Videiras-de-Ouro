from config.data.connection import Conection
from mysql.connector import Error
from decimal import Decimal

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
            with Conection.create_conection() as conn:
                if conn is None:
                    print("ERRO_WINE_CONNECTION: Falha ao conectar ao banco de dados para obter todos os vinhos.")
                    return []
                
                with conn.cursor(dictionary=True) as cursor: 
                    sql = """
                        SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                        FROM tb_produtos p
                        LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                        ORDER BY p.id_produto, i.id_imagem;
                    """
                    cursor.execute(sql)

                    rows = cursor.fetchall() 

                    wines_dict = {}
                    for row in rows:
                        wine_id = row['id_produto']
                        if wine_id not in wines_dict:
                            preco_decimal = Decimal(row['preco']) if row['preco'] is not None else Decimal('0.00')
                            wines_dict[wine_id] = {
                                'id_produto': row['id_produto'],
                                'nome': row['nome'],
                                'preco': preco_decimal,
                                'descricao': row['descricao'],
                                'imagens': []
                            }
                        if row['imagem_url']: 
                            wines_dict[wine_id]['imagens'].append({'url': row['imagem_url']})
                    wines_with_images = list(wines_dict.values())
                    return wines_with_images

        except Error as e:
            print(f"ERRO_WINE_SQL (get_all_wines): Erro no banco de dados ao obter todos os vinhos: {e}")
            return []
        except Exception as e:
            print(f"ERRO_WINE_GERAL (get_all_wines): Erro inesperado ao obter todos os vinhos: {e}")
            return []


    @staticmethod
    def get_wines_by_category(category_id):
        """
        Retorna vinhos de uma categoria específica com suas respectivas imagens.
        Utiliza LEFT JOIN e context managers para garantir o fechamento adequado.
        """
        wines_with_images = []
        try:
            with Conection.create_conection() as conn:
                if conn is None:
                    print(f"ERRO_WINE_CONNECTION: Falha ao conectar ao banco de dados para obter vinhos na categoria {category_id}.")
                    return []

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

                    rows = cursor.fetchall()

                    wines_dict = {}
                    for row in rows:
                        wine_id = row['id_produto']
                        if wine_id not in wines_dict:
                            preco_decimal = Decimal(row['preco']) if row['preco'] is not None else Decimal('0.00')
                            wines_dict[wine_id] = {
                                'id_produto': row['id_produto'],
                                'nome': row['nome'],
                                'preco': preco_decimal,
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
            with Conection.create_conection() as conn:
                if conn is None:
                    print("ERRO_WINE_CONNECTION: Falha ao conectar ao banco de dados para obter vinho por ID.")
                    return None
                with conn.cursor(dictionary=True) as cursor:
                    sql = """
                        SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                        FROM tb_produtos p
                        LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                        WHERE p.id_produto = %s
                        ORDER BY i.id_imagem;
                    """
                    cursor.execute(sql, (wine_id,))

                    rows = cursor.fetchall()

                    if not rows:
                        return None
                    
                    preco_decimal = Decimal(rows[0]['preco']) if rows[0]['preco'] is not None else Decimal('0.00')
                    wine_data = {
                        'id_produto': rows[0]['id_produto'],
                        'nome': rows[0]['nome'],
                        'preco': preco_decimal,
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

