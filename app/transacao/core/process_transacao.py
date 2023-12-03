from models.transacao_model import TransacaoModel
from confluent_kafka import Producer
import json
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from factory.saldo_factory import DAOFactory

class TransactionProcessor:
   
    def __init__(self) -> None:
        self.email_sender = os.getenv("email_sender")
        self.senha_email = os.getenv("senha_email")
        self.saldo_dao = DAOFactory.create_saldo_dao()

    def process_transaction(self, transaction_data: TransacaoModel):
        if transaction_data.valor_base < 1 or type(transaction_data.valor_base) == str: 
            return False
        
        saldo_atual = self.saldo_dao.get_saldo(transaction_data.username)
        if saldo_atual is None or saldo_atual < transaction_data.valor_base:
            raise Exception("Saldo insuficiente")
        
        
        valor_retorno = self.calculate_transaction_amount(transaction_data)
        novo_saldo = valor_retorno + saldo_atual
        self.saldo_dao.update_saldo(transaction_data.username,novo_saldo)

        self.send_email(transaction_data.email, "Transação Registrada", f"Olá {transaction_data.username} Sua transação de {transaction_data.valor_base} foi registrada com sucesso. Seu novo valor é de {novo_saldo}")
        self.produce_message_to_nota_fiscal(transaction_data, novo_saldo, saldo_atual)
        return novo_saldo

    def calculate_transaction_amount(self, transaction_data: TransacaoModel):
        return ((transaction_data.valor_base* transaction_data.valor_base) - transaction_data.valor_base)
    

    def produce_message_to_nota_fiscal(self,transaction_data: TransacaoModel, novo_valor, saldo_atual):
        producer = Producer({'bootstrap.servers': 'localhost:9092'})
        topic = 'nota-fiscal'
        producer.produce(topic, json.dumps({"valor_de":transaction_data.valor_base, "valor_para":novo_valor,
                                             "usuario": transaction_data.username, "saldo_antigo": saldo_atual,
                                             "email": transaction_data.email
                                            }))
        producer.flush()
    
    def send_email(self,receiver_email, subject, body):
        sender_email = self.email_sender
        password = self.senha_email
        print(sender_email)
        print(password)
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        status_code, response = server.ehlo()
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
