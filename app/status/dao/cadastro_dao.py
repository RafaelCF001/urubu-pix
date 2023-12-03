import mysql.connector
from mysql.connector import Error

class CadastroDAO:
    def __init__(self, connection):
        self.connection = connection

    def insert_cadastro(self, username):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO cadastro (username) VALUES (%s)"
            cursor.execute(query, (username,))
            self.connection.commit()  # Confirma a transação
            return cursor.lastrowid  # Retorna o ID do cadastro inserido
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def select_status_cadastro(self, username):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) from cadastro where username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()