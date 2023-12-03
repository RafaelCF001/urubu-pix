from dao.nota_fiscal_dao import NotaFiscalDAO
import mysql.connector

class DAOFactory:
    @staticmethod
    def create_nota_fiscal_dao():
        connection = mysql.connector.connect(
            host='localhost',
            database='nota_fiscal',
            user='ms_nota_fiscal',
            password='123@Mudar'
        )
        return NotaFiscalDAO(connection)
