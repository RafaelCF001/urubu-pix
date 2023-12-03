import mysql.connector
from mysql.connector import Error
from dao.saldo_dao import SaldoDAO

class DAOFactory:
    @staticmethod
    def create_saldo_dao():
        connection_params = {
            'host': 'localhost',
            'database': 'transacoes',
            'user': 'ms_transacao_1',
            'password': '123@Mudar'
        }
        try:
            connection = mysql.connector.connect(**connection_params)
            return SaldoDAO(connection)
        except Error as e:
            print(f"Error ao conectar ao banco de dados: {e}")
            return None
