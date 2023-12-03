
from handler.create_hash import PasswordHasher
from handler.verify_hash import PasswordVerifier
from factory.dao_factory import DAOFactory
from fastapi import FastAPI, HTTPException, status
from models.login_model import LoginData
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
hasher = PasswordHasher()
verifier = PasswordVerifier()
hasher.set_next(verifier)


@router.post("/login")
async def login(login_data: LoginData):
    user_dao = DAOFactory.create_user_dao()
    user = user_dao.get_user_by_name(login_data.username)

    if user:
        verification = hasher.handle({"action": "verify", "password": login_data.password, "hashed_password": user['password']})
        if verification:
            return {"message": "Login Successful"}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
