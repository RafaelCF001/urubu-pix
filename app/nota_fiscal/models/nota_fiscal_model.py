from pydantic import BaseModel

class NotaFiscalModel(BaseModel):
    valor_de: float
    valor_para: float
    usuario:str 
    email: str
    saldo_antigo: float 
                                           