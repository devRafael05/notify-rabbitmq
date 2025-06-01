import pika
import json
import os

host = os.getenv('RABBIT_HOST')
port = int(os.getenv('RABBIT_PORT', 5672))
username = os.getenv('RABBIT_USER')
password = os.getenv('RABBIT_PASS')

exchange = 'whatsapp_exchange'
queue = 'whatsapp_queue'

connection_params = pika.ConnectionParameters(
    host=host,
    port=port,
    credentials=pika.PlainCredentials(username, password)
)

def send_whatsapp_message(wa_data: dict):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(queue=queue, exchange=exchange, routing_key=queue)

    channel.basic_publish(
        exchange=exchange,
        routing_key=queue,
        body=json.dumps(wa_data),
        properties=pika.BasicProperties(delivery_mode=2)  # mensagem persistente
    )

    connection.close()

if __name__ == "__main__":
    wa = {
        "number": "5519989466191@s.whatsapp.net",  # Número do destinatário no formato internacional
        "text": 'Olá, esta é uma mensagem de teste enviada via RabbitMQ!'
        
    }
    send_whatsapp_message(wa)
