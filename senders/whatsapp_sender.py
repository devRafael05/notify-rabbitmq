import requests
import logging
import json

class WhatsAppSender:
    def __init__(self, wa_config):
        self.api_url = wa_config.api_url
        self.api_token = wa_config.api_token
        self.instance_id = wa_config.instance_id

    def send(self, data: dict):
        # Ajustar o payload para conter o campo 'text' diretamente
        payload = {
            "number": data.get("number"),
            "text": data.get("text", "Falha")
        }
        
        url = f"{self.api_url}/message/sendText/{self.instance_id}"

        headers = {
            "apikey": self.api_token,
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(url, json=payload, headers=headers)
            resp.raise_for_status()

            return resp.json()
        except Exception as e:
            logging.error(f"Erro ao enviar mensagem WhatsApp: {e}")
            raise