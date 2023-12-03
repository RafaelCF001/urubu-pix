from fastapi import FastAPI
from confluent_kafka import Consumer, KafkaException
from factory.dao_factory import DAOFactory
from router import routes
import threading
import json


app = FastAPI()

app.include_router(routes.router, prefix='/status')
@app.get("/health")
def main():
    return {"message": "api status is up and running"}


def consumer_kafka(topic):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': '1',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            
            message = json.loads(msg.value())
            print(message)
            if message["topic"] == "cadastro": 
                cadastro_dao = DAOFactory.create_cadastro_dao()
                new_cadastro_id = cadastro_dao.insert_cadastro(message["name"])
                print(f"Cadastro inserido com ID: {new_cadastro_id}")

                pass
            else : 
                nota_fiscal_dao = DAOFactory.create_nota_fiscal_dao()
                new_nota_fiscal_id = nota_fiscal_dao.insert_nota_fiscal(id_compra = message["id_compra"])
                print(f"Nota fiscal inserida com ID: {new_nota_fiscal_id}")



                pass 
    except KafkaException as e:
        print(e)
    finally:
        consumer.close()



# Inicia os consumers em threads separadas
threading.Thread(target=consumer_kafka, args=("cadastro",)).start()
# threading.Thread(target=consumer_kafka, args=("nota-fiscal",)).start()