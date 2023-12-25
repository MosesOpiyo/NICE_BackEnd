import requests
from decouple import config

class ElasticEmailHelper:
    def __init__(self):
        self.api_key = config("ELASTIC_EMAIL_API_KEY")
        self.api_url = config("ELASTIC_EMAIL_API_URL")

    def send_email(self, to, subject, body):
        from_email = config("EMAIL_HOST_USER")
        data = {
            'apikey': self.api_key,
            'from': from_email,
            'subject': subject,
            'to': to,
            'body': body,
            'isTransactional': True,
        }

        response = requests.post(f'{self.api_url}/email/send', data=data)
        return response.json()