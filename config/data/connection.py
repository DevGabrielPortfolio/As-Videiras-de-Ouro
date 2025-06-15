import mysql.connector
from mysql.connector import Error

class Conection:
    # Credênciais do banco de dados local
    _HOST = 'localhost'
    _DATABASE = 'db_vinhas_de_ouro'
    _USER = 'root'  
    _PASSWORD = 'root'
    _PORT = 3306  

    # Credênciais do banco de dados online
    # _HOST = 'asvinhasdeouro-aluno-48a5.c.aivencloud.com'
    # _DATABASE = 'db_vinhas_de_ouro'
    # _USER = 'avnadmin'
    # _PASSWORD = 'AVNS_9WXfOWTT-CeO2uZltgg'
    # _PORT = 14307 

    @staticmethod
    def create_conection():
        try:
            conn = mysql.connector.connect(
                host=Conection._HOST,
                database=Conection._DATABASE,
                user=Conection._USER,
                password=Conection._PASSWORD,
                port=Conection._PORT
            )
            if conn.is_connected():
                print("Conexão bem-sucedida ao banco de dados!")
                return conn
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None # None em caso de falha na conexão
        return None # None se não conectar