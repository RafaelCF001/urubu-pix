from fastapi import APIRouter
from factory.dao_factory import DAOFactory
from dao.cadastro_dao import CadastroDAO
from dao.nota_fiscal_dao import NotaFiscalDAO

router = APIRouter()
cadastro_factory = DAOFactory.create_cadastro_dao() 
nota_fiscal_factory = DAOFactory.create_nota_fiscal_dao()


@router.get("/cadastro/{username}")
def cadastro_status(username):
    if cadastro_factory.select_status_cadastro(username):
        return {"exists": True}
    else:
        return {"exists": False}
    
@router.get("/nota-fiscal/{id_compra}")
async def check_nota_fiscal(id_compra: int):
    if nota_fiscal_factory.nota_fiscal_exists(id_compra):
        return {"exists": True}
    else:
        return {"exists": False}