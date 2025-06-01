import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Configuração de logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self, email_config):
        self.smtp_host = email_config.smtp_server
        self.smtp_port = email_config.smtp_port
        self.smtp_user = email_config.smtp_username
        self.smtp_pass = email_config.smtp_password
        self.from_email = email_config.from_email
        self.use_tls = getattr(email_config, 'use_tls', True)

    def send(self, email_data: dict):
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        to_list = email_data.get('to', [])
        cc_list = email_data.get('cc', [])
        bcc_list = email_data.get('bcc', [])
        recipients = to_list + cc_list + bcc_list
        if not recipients:
            raise ValueError("Nenhum destinatário informado!")
        msg['To'] = ', '.join(to_list)
        if cc_list:
            msg['Cc'] = ', '.join(cc_list)
        msg['Subject'] = email_data.get('subject', '(Sem assunto)')
        msg.attach(MIMEText(email_data.get('html_content', ''), 'html'))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.sendmail(self.from_email, recipients, msg.as_string())
            logger.info(f"Email enviado para: {', '.join(recipients)}")
        except smtplib.SMTPException as e:
            logger.error(f"Falha ao enviar e-mail: {e}")
            raise
