from config.data.connection import Conection

class Comments:
    @staticmethod
    def add_comment(id_usuario, id_produto, comentario_texto):
        try:
            conn = Conection.create_conection()
            cursor = conn.cursor()
            query = """
                INSERT INTO tb_comentarios (id_usuario, id_produto, comentario, data_comentario)
                VALUES (%s, %s, %s, NOW())
            """
            cursor.execute(query, (id_usuario, id_produto, comentario_texto))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao adicionar comentário: {e}")
            return False

    @staticmethod
    def get_comments_by_product_id(id_produto):
        comentarios = []
        try:
            conn = Conection.create_conection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
    c.comentario, 
    c.data_comentario, 
    u.usuario AS usuario
FROM 
    tb_comentarios c
JOIN 
    tb_usuarios u ON c.id_usuario = u.id_usuario
WHERE 
    c.id_produto = %s
ORDER BY 
    c.data_comentario DESC;

            """
            cursor.execute(query, (id_produto,))
            comentarios = cursor.fetchall()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Erro ao buscar comentários: {e}")
        return comentarios