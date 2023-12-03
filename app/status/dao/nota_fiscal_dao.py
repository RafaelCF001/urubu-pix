class NotaFiscalDAO:
    def __init__(self, connection):
        self.connection = connection

    def insert_nota_fiscal(self, id_compra):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO nota_fiscal (id_compra, status) VALUES (%s, %s)"
            status = "realizado"  
            cursor.execute(query, (id_compra, status))
            self.connection.commit()
            return cursor.lastrowid 
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    def nota_fiscal_exists(self, id_compra):
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM nota_fiscal WHERE id_compra = %s"
            cursor.execute(query, (id_compra,))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
