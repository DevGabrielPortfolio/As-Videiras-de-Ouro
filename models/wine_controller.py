from config.data.connection import Conection
from mysql.connector import Error

class Wines:
    @staticmethod
    def get_all_wines():
        conn = None
        cursor = None
        wines = []
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_WINE: Falha ao conectar ao banco de dados para obter todos os vinhos.")
                return []
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                FROM tb_produtos p
                LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                ORDER BY p.nome;
            """
            cursor.execute(sql)
            wines = cursor.fetchall()
            return wines
        except Error as e:
            print(f"ERRO_WINE_SQL: Erro no banco de dados ao obter todos os vinhos: {e}")
            return []
        except Exception as e:
            print(f"ERRO_WINE_GERAL: Erro inesperado ao obter todos os vinhos: {e}")
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
        wines = []
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_WINE: Falha ao conectar ao banco de dados para obter vinhos por categoria.")
                return []
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                FROM tb_produtos p
                JOIN tb_categorias c ON p.id_categoria = c.id_categoria
                LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                WHERE c.id_categoria = %s
                ORDER BY p.nome;
            """
            cursor.execute(sql, (category_id,))
            wines = cursor.fetchall()
            return wines
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

    @staticmethod
    def get_wine_by_id(wine_id):
        conn = None
        cursor = None
        wine = None
        try:
            conn = Conection.create_conection()
            if conn is None:
                return None
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT p.id_produto, p.nome, p.preco, p.descricao, i.url AS imagem_url
                FROM tb_produtos p
                LEFT JOIN tb_imagens i ON p.id_produto = i.id_produto
                WHERE p.id_produto = %s;
            """
            cursor.execute(sql, (wine_id,))
            wine = cursor.fetchone()
            return wine
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