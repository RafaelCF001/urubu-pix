from factory.transaction_factory import DAOFactory
from core.process_transacao import TransactionProcessor
from models.transacao_model import TransacaoModel
class TransactionService:
    def __init__(self):
        self.transaction_dao = DAOFactory.create_transacao_dao()
        self.processor = TransactionProcessor()

    def create_transaction(self, transaction_data: TransacaoModel):
        valor_retorno = self.processor.process_transaction(transaction_data)

        self.transaction_dao.insert_transacao(transaction_data.valor_base,
                                               valor_retorno, transaction_data.username)
        
        return valor_retorno

