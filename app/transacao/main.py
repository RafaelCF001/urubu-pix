from fastapi import FastAPI 
from routes import transacao_routes

app = FastAPI()


app.include_router(transacao_routes.transacao_router, prefix= "/transacao")
