import os
from typing import Dict, Any, Optional
import pika

class RabbitMQConfig:
    def __init__(self):
        self.host = os.getenv('RABBIT_HOST', 'localhost')
        self.port = int(os.getenv('RABBIT_PORT', 5672))
        self.username = os.getenv('RABBIT_USER', 'guest')
        self.password = os.getenv('RABBIT_PASS', 'guest')

    def pika_params(self) -> pika.ConnectionParameters:
        return pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            credentials=pika.PlainCredentials(self.username, self.password)
        )

class EmailConfig:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', '')
        self.use_tls = False

class EvolutionWhatsAppConfig:
    def __init__(self):
        self.api_url = os.getenv('EVOLUTION_API_URL', '')
        self.api_token = os.getenv('EVOLUTION_API_TOKEN', '')
        self.instance_id = os.getenv('EVOLUTION_INSTANCE_ID', '')
        self.webhook_url = os.getenv('EVOLUTION_WEBHOOK_URL', '')
        self.sender = os.getenv('EVOLUTION_SENDER', '')  # se aplicável
        # Você pode adicionar outros campos específicos conforme a documentação

class NotificationConfig:
    def __init__(self):
        self.rabbitmq = RabbitMQConfig()
        self.queues = {
            'email': os.getenv('EMAIL_QUEUE', 'email_queue'),
            'whatsapp': os.getenv('WHATSAPP_QUEUE', 'whatsapp_queue'),
            # outros tipos no futuro...
        }
        self.email = EmailConfig()
        self.whatsapp = EvolutionWhatsAppConfig()
        # Adicione aqui outros canais: self.sms = SMSConfig(), etc

    def get_queue_name(self, notification_type: str) -> str:
        return self.queues.get(notification_type, f"{notification_type}_notifications")

    def get_rabbitmq_connection(self) -> pika.ConnectionParameters:
        return self.rabbitmq.pika_params()

    def get_notification_config(self, notification_type: str) -> Optional[Any]:
        # Exemplo: config.get_notification_config('whatsapp')
        return getattr(self, notification_type, None)
