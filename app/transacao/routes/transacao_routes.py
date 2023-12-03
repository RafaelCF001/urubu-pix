from fastapi import APIRouter
from models.transacao_model import TransacaoModel
from services.transaction_service import TransactionService
from models.saldo_model import SaldoModel
from factory.saldo_factory import DAOFactory
from services.saldo_service import SaldoService
from fastapi.exceptions import HTTPException

transacao_router = APIRouter()
saldo_service = SaldoService(DAOFactory.create_saldo_dao())

@transacao_router.post("/registrar")
def registrar_transacao(transacao_model: TransacaoModel):
    valor_base = transacao_model.valor_base
    user = transacao_model.username

    valor_retorno = TransactionService().create_transaction(transacao_model)

    if valor_retorno != False:
        return {"valor_retorno": f"R$ {valor_retorno}"}

@transacao_router.post("/inserir")
def inserir_saldo(saldo_model: SaldoModel):
    saldo_id = saldo_service.upsert_saldo(saldo_model.usuario, saldo_model.valor)
    if saldo_id:
        return {"id": saldo_id, "status": "Saldo cadastrado com sucesso"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao cadastrar saldo")
