from models.cadastro_model import CadastroModel
from core.validation import Validation
from core.producer.producer import ProducerCadastro
from fastapi import FastAPI, HTTPException, status
from confluent_kafka import Producer

app = FastAPI()
kafka_config  = {"bootstrap.servers":"localhost:9092"}
producer = Producer(kafka_config)
producer_cadastro = ProducerCadastro(producer)

@app.post("/cadastro")
async def login(cadastro_data: CadastroModel):
    print("entrou")
    if cadastro_data != None and cadastro_data.password != None and cadastro_data.type != None:
        if not Validation().validate_username(cadastro_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username format")
    
        if not Validation().validate_password(cadastro_data.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password format")

        producer_cadastro.publish_user_check(cadastro_data.username, cadastro_data.password, cadastro_data.type)

        return {"message": "Cadastro realizado com sucesso"}

    else: 
    
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing data")
