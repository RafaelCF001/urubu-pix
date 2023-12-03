from pydantic import BaseModel

class CadastroModel(BaseModel):
    username: str 
    password: str