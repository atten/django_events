import requests
import json

from django.conf import settings
from urllib.parse import urljoin


class EmailSendError(Exception):
    pass


class DBMailerAPI:
    def __init__(self, api_key='', root_url=''):
        self.api_key = api_key or getattr(settings, 'DB_MAILER_API_KEY', None)
        assert self.api_key, 'Where is my API Key?'

        self.root_url = root_url or getattr(settings, 'DB_MAILER_ROOT_URL', None)
        assert self.api_key, 'Where is my root url?'

        self.send_api_url = urljoin(self.root_url, '/dbmail/api/')

    def send(self, slug: str, recipient: str, context: dict):
        bundle = {
            'data': json.dumps(context),
            'api_key': self.api_key,
            'recipient': recipient,
            'slug': slug
        }
        r = requests.post(self.send_api_url, bundle)
        if r.text != 'OK':
            raise EmailSendError()
