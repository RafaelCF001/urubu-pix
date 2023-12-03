
from fastapi import FastAPI
from handler.create_hash import PasswordHasher
from factory.dao_factory import DAOFactory
from confluent_kafka import Consumer, KafkaException, Producer
from routes import login_routes
from threading import Thread
import json

kafka_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': '1',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(kafka_config)
consumer.subscribe(['login-cadastro'])

app = FastAPI()
app.include_router(login_routes.router, prefix='/urubu')

@app.get("/health")
def main():
    return {"message":"API is up and running"}

def consume():
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(msg.error())
                break
                
            payload = msg.value().decode('utf-8')
            payload = json.loads(payload)
            print(payload)
            user_dao = DAOFactory.create_user_dao()
            user = user_dao.user_exists(payload["username"])
            print(user)
            if user: 
                produce(user,payload["username"])
            else:
                hasher = PasswordHasher()
                hashed_password = hasher.handle({
                "action": "hash",
                "password": payload["password"]
                })
                id = user_dao.insert_user(payload["username"], hashed_password, payload["type"])
                print(id)
                produce(user, payload["username"])
               

    except KafkaException as e:
        print(e)
    finally:
        consumer.close()

def produce(condition: bool,name ) -> None:
    kafka_config  = {"bootstrap.servers":"localhost:9092"}
    producer = Producer(kafka_config)
    producer.produce('cadastro', key=name, value=json.dumps({"condition":condition, "name":name, "topic": "cadastro"}))
    producer.poll(0)
    producer.flush()


consumer_thread = Thread(target=consume)
consumer_thread.start()