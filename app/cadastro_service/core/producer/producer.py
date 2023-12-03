import json

class ProducerCadastro():
    
    def __init__(self, producer) -> None:
        self.producer = producer

    def delivery_report(self,err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def publish_user_check(self,username, password, type):
        print("entrou 2 ")
        self.producer.produce('login-cadastro', key=username, value=json.dumps({"username":username,"password":password, "type":type}), callback=self.delivery_report)
        self.producer.poll(0)
        self.producer.flush()
        return "deu certo"
    