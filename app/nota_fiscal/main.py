from confluent_kafka import Consumer, KafkaException
from factory.nota_fiscal_factory import DAOFactory
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json
import smtplib
import os 

def create_pdf(filename, data):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, f"Usuario: {data['usuario']}")
    c.drawString(100, height - 120, f"Valor De: {data['valor_de']}")
    c.drawString(100, height - 140, f"Valor Para: {data['valor_para']}")

    c.save()



def send_email_with_pdf(receiver_email, subject, body, pdf_path):
    sender_email = os.getenv("email")
    password = os.getenv("senha")

    # Configurando a mensagem
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Anexando o PDF
    with open(pdf_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {pdf_path}")
    message.attach(part)

    # Enviando o e-mail
    server = smtplib.SMTP("smtp-mail.outlook.com", 587)
    status_code, response = server.ehlo()
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


def nota_fiscal_consumer():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'nota-fiscal',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['nota-fiscal'])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            message = json.loads(msg.value())
            usuario = message["usuario"]
            valor_de = message["valor_de"]
            valor_para = message["valor_para"]

            nota_fiscal_dao = DAOFactory.create_nota_fiscal_dao()
            nota_fiscal_dao.insert_nota_fiscal(usuario, valor_de, valor_para)
            pdf_filename = "Nota_Fiscal.pdf"
            create_pdf(pdf_filename, message)
            send_email_with_pdf(message["email"], "Sua Nota Fiscal", "Segue anexo a nota fiscal.", pdf_filename)
    except KafkaException as e:
        print(e)
    finally:
        consumer.close()

if __name__ == "__main__":
    nota_fiscal_consumer()
