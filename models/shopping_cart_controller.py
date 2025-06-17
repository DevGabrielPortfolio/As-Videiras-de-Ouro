from config.data.connection import Conection
from mysql.connector import Error

class ControlShoppingCart:

    @staticmethod
    def adicionar_ou_atualizar_item(id_usuario, id_produto, quantidade):
        conn = None
        cursor = None
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_CSC: Falha ao obter conexão para adicionar/atualizar item no carrinho.")
                return False

            cursor = conn.cursor()
            print("DEBUG_CSC: Conexão e cursor criados. Início da transação.")

            sql_check = "SELECT id_item_carrinho, quantidade FROM tb_itens_carrinho WHERE id_usuario = %s AND id_produto = %s;"
            print(f"DEBUG_CSC: Executando SELECT: {sql_check} com user={id_usuario}, prod={id_produto}")
            cursor.execute(sql_check, (id_usuario, id_produto))
            item_existente = cursor.fetchone()

            if item_existente:
                id_item_carrinho_existente = item_existente[0]
                quantidade_atual = item_existente[1]
                nova_quantidade = quantidade_atual + quantidade

                sql_update = "UPDATE tb_itens_carrinho SET quantidade = %s WHERE id_item_carrinho = %s;"
                print(
                    f"DEBUG_CSC: Item existente. Executando UPDATE: {sql_update} com qtd={nova_quantidade}, id_item={id_item_carrinho_existente}")
                cursor.execute(sql_update, (nova_quantidade, id_item_carrinho_existente))
                print(
                    f"DEBUG_CSC: Cursor rowcount após UPDATE: {cursor.rowcount}")
            else:
                sql_insert = "INSERT INTO tb_itens_carrinho (id_usuario, id_produto, quantidade) VALUES (%s, %s, %s);"
                print(
                    f"DEBUG_CSC: Item NÃO existente. Executando INSERT: {sql_insert} com user={id_usuario}, prod={id_produto}, qtd={quantidade}")
                cursor.execute(sql_insert, (id_usuario, id_produto, quantidade))
                print(f"DEBUG_CSC: Cursor lastrowid após INSERT: {cursor.lastrowid}")
                print(f"DEBUG_CSC: Cursor rowcount após INSERT: {cursor.rowcount}")

            conn.commit()
            print("DEBUG_CSC: Transação commitada com sucesso! (Isso deveria salvar no DB)")
            return True

        except Error as e:
            print(f"ERRO_CSC_SQL: Erro no banco de dados AO TENTAR COMMITAR OU EXECUTAR QUERY: {e}")
            if conn:
                conn.rollback()
                print("DEBUG_CSC: Rollback executado devido a erro.")
            return False
        except Exception as e:
            print(f"ERRO_CSC_GERAL: Erro inesperado AO TENTAR COMMITAR OU EXECUTAR QUERY: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("DEBUG_CSC: Conexão com DB fechada.")


    @staticmethod
    def get_itens_carrinho_por_usuario(id_usuario):
        conn = None
        cursor = None
        itens_carrinho = []
        try:
            conn = Conection.create_conection()
            if conn is None:
                print(
                    "ERRO: Falha ao conectar ao banco de dados para obter itens do"
                    " carrinho."
                )
                return []
            cursor = conn.cursor(dictionary=True)
            sql = """
                  SELECT p.id_produto,
                         p.nome                   AS nome_produto, \
                         p.preco                  AS preco_unitario, \
                         i.quantidade, \
                         (p.preco * i.quantidade) AS valor_total, \
                         img.url                  AS imagem_produto
                  FROM tb_itens_carrinho i
                           JOIN tb_produtos p ON i.id_produto = p.id_produto
                           LEFT JOIN tb_imagens img ON p.id_produto = img.id_produto
                  WHERE i.id_usuario = %s
                  GROUP BY p.id_produto, i.quantidade, img.url
                  ORDER BY i.id_item_carrinho; \
                  """
            cursor.execute(sql, (id_usuario,))
            itens_carrinho = cursor.fetchall()
            return itens_carrinho
        except Error as e:
            print(f"Erro no banco de dados ao obter itens do carrinho: {e}")
            return []
        except Exception as e:
            print(f"Erro inesperado ao obter itens do carrinho: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("DEBUG_CS: Conexão fechada após obter itens do carrinho.")

    @staticmethod
    def remover_item_carrinho(id_usuario, id_produto):
        conn = None
        cursor = None
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_CSC: Falha ao obter conexão para remover item do carrinho.")
                return False

            cursor = conn.cursor()
            sql_delete = "DELETE FROM tb_itens_carrinho WHERE id_usuario = %s AND id_produto = %s;"
            cursor.execute(sql_delete, (id_usuario, id_produto))
            conn.commit()
            print(
                f"DEBUG_CSC: Item (usuário: {id_usuario}, produto: {id_produto}) removido do carrinho. Linhas afetadas: {cursor.rowcount}")
            return cursor.rowcount > 0
        except Error as e:
            print(f"ERRO_CSC_SQL: Erro no banco de dados ao remover item do carrinho: {e}")
            if conn:
                conn.rollback()
            return False
        except Exception as e:
            print(f"ERRO_CSC_GERAL: Erro inesperado ao remover item do carrinho: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("DEBUG_CSC: Conexão com DB fechada após remover item.")

    @staticmethod
    def atualizar_quantidade_item(id_usuario, id_produto, nova_quantidade):
        conn = None
        cursor = None
        try:
            conn = Conection.create_conection()
            if conn is None:
                print("ERRO_CSC: Falha ao obter conexão para atualizar quantidade do item.")
                return False

            cursor = conn.cursor()
            if nova_quantidade < 1:
                nova_quantidade = 1

            sql_update = """
                         UPDATE tb_itens_carrinho
                         SET quantidade = %s
                         WHERE id_usuario = %s \
                           AND id_produto = %s; \
                         """
            cursor.execute(sql_update, (nova_quantidade, id_usuario, id_produto))
            conn.commit()
            print(
                f"DEBUG_CSC: Quantidade do item (usuário: {id_usuario}, produto: {id_produto}) atualizada para {nova_quantidade}. Linhas afetadas: {cursor.rowcount}")
            return cursor.rowcount > 0
        except Error as e:
            print(f"ERRO_CSC_SQL: Erro no banco de dados ao atualizar quantidade do item: {e}")
            if conn:
                conn.rollback()
            return False
        except Exception as e:
            print(f"ERRO_CSC_GERAL: Erro inesperado ao atualizar quantidade do item: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
                print("DEBUG_CSC: Conexão com DB fechada após atualizar quantidade.")


    @staticmethod
    def clear_cart(id_usuario):
        try:
            conn = Conection.create_conection()
            cursor = conn.cursor()
            query = "DELETE FROM tb_itens_carrinho WHERE id_usuario = %s;"
            cursor.execute(query, (id_usuario,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao limpar o carrinho para o usuário {id_usuario}: {e}")
            return False