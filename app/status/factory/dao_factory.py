import mysql.connector
from dao.cadastro_dao import CadastroDAO
from dao.nota_fiscal_dao import NotaFiscalDAO
class DAOFactory:
    @staticmethod
    def create_cadastro_dao():
        connection_params = {
            'host': 'localhost',
            'database': 'status',
            'user': 'ms_status_!',
            'password': '123@Mudar'
        }
        connection = mysql.connector.connect(**connection_params)
        return CadastroDAO(connection)
    
    @staticmethod
    def create_nota_fiscal_dao():
        connection_params = {
            'host': 'localhost',
            'database': 'status',
            'user': 'ms_status_!',
            'password': '123@Mudar'
        }
        connection = mysql.connector.connect(**connection_params)
        return NotaFiscalDAO(connection)
