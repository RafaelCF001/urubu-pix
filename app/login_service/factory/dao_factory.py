from dao.user_dao import UserDAO
import mysql.connector

class DAOFactory:
    @staticmethod
    def create_user_dao():
        connection = mysql.connector.connect(
            host='localhost',
            database='users',
            user='ms_users_1',
            password='123@Mudar'
        )
        return UserDAO(connection)
