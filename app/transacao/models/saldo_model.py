from pydantic import BaseModel

class SaldoModel(BaseModel):
    valor: float
    usuario: str