from config.data.connection import Conection
from mysql.connector import Error

class Categories:
    @staticmethod
    def get_all_categories():
        conn = None
        cursor = None
        categories = []
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_CAT: Falha ao conectar ao banco de dados para obter categorias.")
                return []
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT id_categoria, nome FROM tb_categorias ORDER BY nome;"
            cursor.execute(sql)
            categories = cursor.fetchall()
            return categories
        except Error as e:
            print(f"ERRO_CAT_SQL: Erro no banco de dados ao obter categorias: {e}")
            return []
        except Exception as e:
            print(f"ERRO_CAT_GERAL: Erro inesperado ao obter categorias: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()