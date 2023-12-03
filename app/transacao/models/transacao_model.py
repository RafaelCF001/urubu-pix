from pydantic import BaseModel


class TransacaoModel(BaseModel):
    valor_base: float
    username: str 
    email: str