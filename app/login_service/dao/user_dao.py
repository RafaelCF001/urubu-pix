import mysql.connector
from mysql.connector import Error

class UserDAO:
    def __init__(self, connection):
        self.connection = connection

    def get_user_by_name(self, username):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE name = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def user_exists(self, username):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT COUNT(*) FROM users WHERE name = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result["COUNT(*)"] > 0
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()

    def insert_user(self, username, password, user_type):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO users (name, password, type) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, user_type))
            self.connection.commit()  
            return cursor.lastrowid  
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()