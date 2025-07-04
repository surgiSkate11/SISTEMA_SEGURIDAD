import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

PAYPAL_API_BASE = getattr(settings, 'PAYPAL_API_BASE', 'https://api-m.sandbox.paypal.com')
PAYPAL_CURRENCY = getattr(settings, 'PAYPAL_CURRENCY', 'USD')

class PayPalAPI:
    def __init__(self):
        self.client_id = getattr(settings, 'PAYPAL_CLIENT_ID', None)
        self.secret = getattr(settings, 'PAYPAL_SECRET', None)
        self.base_url = getattr(settings, 'PAYPAL_API_BASE', PAYPAL_API_BASE)
        if not self.client_id or not self.secret:
            raise ImproperlyConfigured('Debes definir PAYPAL_CLIENT_ID y PAYPAL_SECRET en settings.py')
        self.token = self.get_access_token()

    def get_access_token(self):
        resp = requests.post(
            f'{self.base_url}/v1/oauth2/token',
            auth=(self.client_id, self.secret),
            data={'grant_type': 'client_credentials'},
        )
        if resp.status_code != 200:
            raise Exception(f'Error autenticando con PayPal: {resp.text}')
        return resp.json()['access_token']

    def create_order(self, amount, currency=None, return_url='', cancel_url=''):
        currency = currency or PAYPAL_CURRENCY
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'intent': 'CAPTURE',
            'purchase_units': [{
                'amount': {
                    'currency_code': currency,
                    'value': f'{amount:.2f}'
                }
            }],
            'application_context': {
                'return_url': return_url,
                'cancel_url': cancel_url
            }
        }
        resp = requests.post(f'{self.base_url}/v2/checkout/orders', json=data, headers=headers)
        if resp.status_code not in (200, 201):
            raise Exception(f'Error creando orden PayPal: {resp.text}')
        return resp.json()

    def capture_order(self, order_id):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        resp = requests.post(f'{self.base_url}/v2/checkout/orders/{order_id}/capture', headers=headers)
        if resp.status_code not in (200, 201):
            raise Exception(f'Error capturando orden PayPal: {resp.text}')
        return resp.json()
