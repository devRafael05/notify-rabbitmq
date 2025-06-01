import pika
import json
import os

host = os.getenv('RABBIT_HOST')
port = int(os.getenv('RABBIT_PORT', 5672))
username = os.getenv('RABBIT_USER')
password = os.getenv('RABBIT_PASS')

exchange = 'email_exchange'
queue = 'email_queue'

connection_params = pika.ConnectionParameters(
    host=host,
    port=port,
    credentials=pika.PlainCredentials(username, password)
)

def send_email_message(email_data: dict):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(queue=queue, exchange=exchange, routing_key=queue)

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=json.dumps(email_data),
        properties=pika.BasicProperties(delivery_mode=2)  # mensagem persistente
    )
    print('Mensagem de email publicada no RabbitMQ')
    connection.close()

if __name__ == "__main__":
    email = {
        "to": ["rafaelsilva.dev05@gmail.com"],
        "subject": "Teste envio via RabbitMQ2",
        "html_content": "<h1>Olá!</h1><p>Este é um email enviado via RabbitMQ.</p>"
    }
    send_email_message(email)