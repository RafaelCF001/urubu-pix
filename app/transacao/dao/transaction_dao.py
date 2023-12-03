import mysql.connector
from mysql.connector import Error

class TransacaoDAO:
    def __init__(self, connection):
        self.connection = connection

    def insert_transacao(self, valor_base, valor_retorno, usuario):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO transacoes (valor_base, valor_retorno, usuario) VALUES (%s, %s, %s)"
            cursor.execute(query, (valor_base, valor_retorno, usuario))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def get_transacao(self, usuario):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM transacoes WHERE usuario = %s"
            cursor.execute(query, (usuario,))
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def update_transacao(self, transacao_id, valor_base=None, valor_retorno=None, usuario=None):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "UPDATE transacoes SET valor_base = %s, valor_retorno = %s, usuario = %s WHERE id = %s"
            cursor.execute(query, (valor_base, valor_retorno, usuario, transacao_id))
            self.connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def delete_transacao(self, transacao_id):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM transacoes WHERE id = %s"
            cursor.execute(query, (transacao_id,))
            self.connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
