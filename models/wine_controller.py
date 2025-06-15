from config.data.connection import Conection
from mysql.connector import Error

class Wines:

    @staticmethod
    def get_all_wines():
        conn = None
        cursor = None
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_WINE: Falha ao conectar ao banco de dados para obter vinhos.")
                return []

            cursor = conn.cursor(dictionary=True)

            # 1. Buscar todos os vinhos
            sql_vinhos = """
                SELECT id_produto, nome, preco, descricao
                FROM tb_produtos
                ORDER BY nome;
            """
            cursor.execute(sql_vinhos)
            vinhos = cursor.fetchall()

            # 2. Buscar todas as imagens
            sql_imagens = """
                SELECT id_produto, url
                FROM tb_imagens;
            """
            cursor.execute(sql_imagens)
            imagens = cursor.fetchall()

            # 3. Agrupar imagens por id_produto
            imagens_por_produto = {}
            for img in imagens:
                imagens_por_produto.setdefault(img['id_produto'], []).append({'url': img['url']})

            # 4. Associar imagens aos vinhos
            for vinho in vinhos:
                vinho['imagens'] = imagens_por_produto.get(vinho['id_produto'], [])

            return vinhos

        except Error as e:
            print(f"ERRO_WINE_SQL: {e}")
            return []
        except Exception as e:
            print(f"ERRO_WINE_GERAL: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()





    @staticmethod
    def get_wines_by_category(category_id):
        conn = None
        cursor = None
        wines_with_images = [] # Lista final de vinhos com suas imagens agrupadas
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_WINE: Falha ao conectar ao banco de dados para obter vinhos por categoria.")
                return []
            cursor = conn.cursor(dictionary=True) # Retorna dicionários

            # 1. Buscar vinhos e suas imagens por categoria
            # Use LEFT JOIN para garantir que vinhos sem imagens também sejam retornados
            sql = """
                SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                FROM tb_produtos p
                LEFT JOIN tb_categorias c ON p.id_categoria = c.id_categoria
                LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                WHERE c.id_categoria = %s
                ORDER BY p.id_produto, i.id_imagem; -- Importante para agrupar as imagens do mesmo produto
            """
            cursor.execute(sql, (category_id,))
            rows = cursor.fetchall()

            # 2. Agrupar os dados para associar múltiplas imagens a cada vinho
            wines_dict = {}
            for row in rows:
                wine_id = row['id_produto']
                if wine_id not in wines_dict:
                    # Se o vinho ainda não foi adicionado, crie a entrada
                    wines_dict[wine_id] = {
                        'id_produto': row['id_produto'],
                        'nome': row['nome'],
                        'preco': row['preco'],
                        'descricao': row['descricao'],
                        'imagens': [] # Inicializa a lista de imagens
                    }
                # Adiciona a URL da imagem à lista de imagens do vinho, se ela existir
                if row['imagem_url']:
                    wines_dict[wine_id]['imagens'].append({'url': row['imagem_url']})

            # Converte o dicionário de vinhos de volta para uma lista
            wines_with_images = list(wines_dict.values())
            return wines_with_images

        except Error as e:
            print(f"ERRO_WINE_SQL: Erro no banco de dados ao obter vinhos por categoria: {e}")
            return []
        except Exception as e:
            print(f"ERRO_WINE_GERAL: Erro inesperado ao obter vinhos por categoria: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    # ... (Seu método get_wine_by_id() - está quase correto, mas precisa de um ajuste para 'imagens') ...

    @staticmethod
    def get_wine_by_id(wine_id):
        conn = None
        cursor = None
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_WINE: Falha ao conectar ao banco de dados para obter vinho por ID.")
                return None
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                FROM tb_produtos p
                LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                WHERE p.id_produto = %s
                ORDER BY i.id_imagem; -- Para garantir uma ordem para as imagens
            """
            cursor.execute(sql, (wine_id,))
            rows = cursor.fetchall() # Fetch all rows, as a wine can have multiple images

            if not rows:
                return None # Vinho não encontrado

            # Agrupar as imagens para o vinho único
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
            print(f"ERRO_WINE_SQL: Erro no banco de dados ao obter vinho por ID: {e}")
            return None
        except Exception as e:
            print(f"ERRO_WINE_GERAL: Erro inesperado ao obter vinho por ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
