
class SaldoService:
    def __init__(self, saldo_dao):
        self.saldo_dao = saldo_dao

    def upsert_saldo(self, usuario, valor):
        return self.saldo_dao.upsert_saldo(usuario, valor)