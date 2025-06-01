import logging
import signal
import sys
import threading
import time
from config import NotificationConfig
from utils.consumer import NotificationConsumer
from senders.email_sender import EmailSender
from senders.whatsapp_sender import WhatsAppSender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

threads = []
consumers = []

def run_consumer(consumer):
    consumer.start()

def main():
    config = NotificationConfig()

    # Email
    email_sender = EmailSender(config.email)
    email_consumer = NotificationConsumer(
        rabbitmq_conn_params=config.get_rabbitmq_connection(),
        queue_name=config.get_queue_name('email'),
        exchange='email_exchange',
        sender=email_sender
    )
    consumers.append(email_consumer)

    # WhatsApp
    whatsapp_sender = WhatsAppSender(config.whatsapp)
    whatsapp_consumer = NotificationConsumer(
        rabbitmq_conn_params=config.get_rabbitmq_connection(),
        queue_name=config.get_queue_name('whatsapp'),
        exchange='whatsapp_exchange',
        sender=whatsapp_sender,
        callback_validate=lambda data: bool(data.get('number') and data.get('text'))
    )
    consumers.append(whatsapp_consumer)

    # Cria uma thread para cada consumer
    for cons in consumers:
        t = threading.Thread(target=run_consumer, args=(cons,))
        t.daemon = True  # Importante para encerrar junto
        t.start()
        threads.append(t)

    def graceful_shutdown(signum, frame):
        logging.info("Recebido sinal de shutdown. Parando consumers...")
        for cons in consumers:
            cons.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)

    # Windows-friendly: mantém o processo vivo para capturar sinais
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        graceful_shutdown(None, None)

if __name__ == "__main__":
    main()
    logging.info("Iniciando o serviço de notificações...")