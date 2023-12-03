class NotaFiscalDAO:
    def __init__(self, connection):
        self.connection = connection

    def insert_nota_fiscal(self, usuario, valor_de, valor_para):
        cursor = None
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO nota_fiscal (usuario, valor_de, valor_para) VALUES (%s, %s, %s)"
            cursor.execute(query, (usuario, valor_de, valor_para))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
