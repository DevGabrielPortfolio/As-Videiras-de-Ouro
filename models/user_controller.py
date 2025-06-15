from config.data.connection import Conection
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash


class Users:

    @staticmethod
    def register_user(username, password_plaintext, telefone, email, cep, rua, numero, bairro, cidade, estado):
        try:
            conn = Conection.create_conection()
            cursor = conn.cursor(dictionary=True)

            sql_check_existence = "SELECT id_usuario FROM tb_usuarios WHERE usuario = %s OR email = %s"
            cursor.execute(sql_check_existence, (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                print(f"Tentativa de registro falha: Usuário '{username}' ou e-mail '{email}' já cadastrado.")
                return None  # Indica que o usuário já existe

            hashed_password = generate_password_hash(password_plaintext)

            sql_insert_user = "INSERT INTO tb_usuarios(usuario, senha, telefone, email) VALUES (%s, %s, %s, %s)"
            values_user = (username, hashed_password, telefone, email)
            cursor.execute(sql_insert_user, values_user)

            user_id = cursor.lastrowid

            if user_id:
                sql_insert_address = "INSERT INTO tb_enderecos(id_usuario, cep, rua, numero, bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values_address = (user_id, cep, rua, numero, bairro, cidade, estado)
                cursor.execute(sql_insert_address, values_address)

                conn.commit()  # Confirma ambas as inserções
                print(f"Usuário '{username}' e endereço cadastrados com sucesso. ID: {user_id}")
                return user_id  # Retorna o ID do usuário em caso de sucesso
            else:
                # Este caso é raro, indica que o INSERT do usuário falhou silenciosamente
                print(f"Erro: Não foi possível obter o ID do usuário após a inserção para '{username}'.")
                conn.rollback()  # Desfaz a inserção do usuário
                return None

        except Error as e:  # Erros específicos do MySQL Connector
            print(f'Erro no banco de dados ao registrar usuário: {e}')
            if conn and conn.is_connected():
                conn.rollback()  # Desfaz operações em caso de erro de DB
            return None
        except Exception as e:  # Outros erros inesperados
            print(f'Erro inesperado na classe Users.register_user: {e}')
            if conn and conn.is_connected():
                conn.rollback()  # Desfaz operações em caso de erro inesperado
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    @staticmethod
    def verify_user_credentials(login_identifier, password_plaintext):
        conn = None
        cursor = None
        try:
            conn = Conection.create_conection()
            cursor = conn.cursor(dictionary=True)

            sql = "SELECT id_usuario, usuario, senha FROM tb_usuarios WHERE usuario = %s OR email = %s"
            cursor.execute(sql, (login_identifier, login_identifier))
            user_data = cursor.fetchone()

            if user_data:
                stored_hashed_password = user_data['senha']

                if check_password_hash(stored_hashed_password, password_plaintext):
                    print(f"Login bem-sucedido para: {user_data['usuario']}")
                    return (user_data['id_usuario'], user_data['usuario'])
                else:
                    # Senha incorreta
                    print(f"Tentativa de login falha: Senha incorreta para: {login_identifier}")
                    return None
            else:
                # Usuário ou e-mail não encontrado
                print(f"Tentativa de login falha: Usuário ou e-mail não encontrado: {login_identifier}")
                return None

        except Error as e:
            print(f'Erro no banco de dados ao verificar credenciais: {e}')
            return None
        except Exception as e:
            print(f'Erro inesperado na classe Users.verify_user_credentials: {e}')
            return None
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()