import mysql.connector
from mysql.connector import Error
from dao.transaction_dao import TransacaoDAO

class DAOFactory:
    @staticmethod
    def create_transacao_dao():
        connection_params = {
            'host': 'localhost',
            'database': 'transacoes',
            'user': 'ms_transacao_1',
            'password': '123@Mudar'
        }
        try:
            connection = mysql.connector.connect(**connection_params)
            return TransacaoDAO(connection)
        except Error as e:
            print(f"Error ao conectar ao banco de dados: {e}")
            return None
