import mysql.connector
from mysql.connector import Error

class SaldoDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_saldo(self, usuario):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "SELECT valor FROM saldo WHERE usuario = %s"
            cursor.execute(query, (usuario,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def update_saldo(self, usuario, novo_valor):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "UPDATE saldo SET valor = %s WHERE usuario = %s"
            cursor.execute(query, (novo_valor, usuario))
            self.connection.commit()
            return cursor.rowcount
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()

    def upsert_saldo(self, usuario, valor):
        cursor = None
        try:
            cursor = self.connection.cursor()
            select_query = "SELECT valor FROM saldo WHERE usuario = %s"
            cursor.execute(select_query, (usuario,))
            result = cursor.fetchone()

            if result:
                novo_valor = result[0] + valor
                update_query = "UPDATE saldo SET valor = %s WHERE usuario = %s"
                cursor.execute(update_query, (novo_valor, usuario))
            else:
                insert_query = "INSERT INTO saldo (usuario, valor) VALUES (%s, %s)"
                cursor.execute(insert_query, (usuario, valor))

            self.connection.commit()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()