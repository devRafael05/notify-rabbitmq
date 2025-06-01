import json
import logging
import pika

logger = logging.getLogger(__name__)

class NotificationConsumer:
    def __init__(self, rabbitmq_conn_params, queue_name, exchange, sender, callback_validate=None):
        self.rabbitmq_conn_params = rabbitmq_conn_params
        self.queue_name = queue_name
        self.exchange = exchange
        self.sender = sender
        self.callback_validate = callback_validate or self.default_validate
        self.connection = None
        self.channel = None

    def default_validate(self, data):
        # Implementação padrão: espera campo 'to'
        return bool(data.get('to'))

    def callback(self, ch, method, properties, body):

        try:
            data = json.loads(body.decode('utf-8'))

            print(f"Dados recebidos: {data}")
            if not self.callback_validate(data):
                logger.error("Payload inválido para esta notificação.")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                return
            self.sender.send(data)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except json.JSONDecodeError:
            logger.error("Payload inválido (JSON).")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start(self):
        self.connection = pika.BlockingConnection(self.rabbitmq_conn_params)
        self.channel = self.connection.channel()

        # Garantir Exchange e Queue
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct', durable=True)
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange, routing_key=self.queue_name)

        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
        try:
            self.channel.start_consuming()

        finally:
            self.stop()

    def stop(self):
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()
        if self.connection and self.connection.is_open:
            self.connection.close()
        logger.info("Consumer finalizado.")
