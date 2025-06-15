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
