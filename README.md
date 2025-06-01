# 🚀 Notify Service

**Notify Service** é um microserviço em Python para envio de notificações assíncronas via **e-mail** e **WhatsApp** usando RabbitMQ como fila.
Ideal para orquestrar notificações transacionais e marketing em qualquer aplicação moderna!

---

## ✨ Principais Recursos

* **Envio de e-mails** com suporte a HTML, múltiplos destinatários e cópia oculta.
* **Envio de mensagens WhatsApp** via Evolution API.
* **Escalável** — múltiplos consumidores (email/zap) trabalhando em paralelo via threading.
* **Configuração via `.env`** e variáveis de ambiente para fácil deploy em diferentes ambientes.
* **Pronto para Docker** e produção!

---

## 🏗️ Estrutura do Projeto

```
notify_service/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── config.py
├── consumer.py
├── senders/
│   ├── email_sender.py
│   └── whatsapp_sender.py
└── .env
```

---

## 🚦 Como Usar

### 1. **Configure as variáveis de ambiente**

Crie um arquivo `.env` baseado no exemplo:

```env
# RabbitMQ
RABBIT_HOST=seu_rabbitmq
RABBIT_PORT=5672
RABBIT_USER=guest
RABBIT_PASS=guest

# E-mail
SMTP_SERVER=smtp.seudominio.com
SMTP_PORT=587
SMTP_USERNAME=seuemail@seudominio.com
SMTP_PASSWORD=suasenha
FROM_EMAIL=seuemail@seudominio.com

# WhatsApp (Evolution API)
WHATSAPP_API_URL=https://evo.zerusbarber.com.br
WHATSAPP_API_TOKEN=SEU_TOKEN_AQUI
WHATSAPP_INSTANCE_ID=ZerusBarber
```

---

### 2. **Build e execute via Docker Compose**

```bash
docker-compose up --build -d
```

### 3. **Logs em tempo real**

```bash
docker logs -f notify_service
```

---

### 4. **Publicar mensagem na fila (exemplo Python)**

#### **E-mail**

```python
import pika, json, os

conn = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv('RABBIT_HOST', 'localhost'),
    port=int(os.getenv('RABBIT_PORT', 5672)),
    credentials=pika.PlainCredentials(
        os.getenv('RABBIT_USER', 'guest'),
        os.getenv('RABBIT_PASS', 'guest'))
))
ch = conn.channel()
ch.basic_publish(
    exchange='email_exchange',
    routing_key='email_queue',
    body=json.dumps({
        "to": ["destinatario@email.com"],
        "subject": "Testando Notify Service",
        "html_content": "<h1>Olá, mundo!</h1>"
    }),
    properties=pika.BasicProperties(delivery_mode=2)
)
conn.close()
```

#### **WhatsApp**

```python
import pika, json, os

conn = pika.BlockingConnection(pika.ConnectionParameters(
    host=os.getenv('RABBIT_HOST', 'localhost'),
    port=int(os.getenv('RABBIT_PORT', 5672)),
    credentials=pika.PlainCredentials(
        os.getenv('RABBIT_USER', 'guest'),
        os.getenv('RABBIT_PASS', 'guest'))
))
ch = conn.channel()
ch.basic_publish(
    exchange='whatsapp_exchange',
    routing_key='whatsapp_queue',
    body=json.dumps({
        "number": "5511999998888@s.whatsapp.net",
        "textMessage": {"text": "Olá, esta é uma mensagem via Notify Service!"}
    }),
    properties=pika.BasicProperties(delivery_mode=2)
)
conn.close()
```

---

## 👩‍💻 Colabore!

Pull requests e sugestões são muito bem-vindos.
Para dúvidas ou bugs, abra uma Issue.

---

