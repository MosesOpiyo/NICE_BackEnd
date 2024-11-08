import requests
import json
from decouple import config
from paypalrestsdk import Payment

from .models import Subscription

def make_paypal_payment(receipt):
    # Set up PayPal API credentials
    client_id = config("PAYPAL_CLIENT_ID")
    secret = config("PAYPAL_SECRET")
    url =config("PAYPAL_BASE_URL")
    # Set up API endpoints
    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    payment_url = base_url + '/v1/payments/payment'

    currency = 'USD'

    return_url = 'https://nicedirectcoffee.com/payment/paypal/success/'
    cancel_url = 'https://nicedirectcoffee.com'

    # Request an access token
    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        return False,"Failed to authenticate with PayPal API",None

    access_token = token_response.json()['access_token']

    # Create payment payload
    payment_payload = {
        'intent': 'sale',
        'payer': {'payment_method': 'paypal'},
        'transactions': [{
            'amount': {'total': str(receipt.amount), 'currency': currency},
            'description': 'Vulnvision scan & protect '
        }],
        'redirect_urls': {
            'return_url': return_url,
            'cancel_url': cancel_url
        }
    }

    # Create payment request
    payment_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payment_response = requests.post(payment_url, data=json.dumps(payment_payload), headers=payment_headers)
    if payment_response.status_code != 201:
        return False , 'Failed to create PayPal payment.',None

    payment_id = payment_response.json()['id']
    approval_url = next(link['href'] for link in payment_response.json()['links'] if link['rel'] == 'approval_url')

    return True,payment_id, approval_url

def verify_paypal_payment(payment_id):
    # Set up PayPal API credentials
    client_id = config("PAYPAL_CLIENT_ID")
    secret = config("PAYPAL_SECRET")
    url =config("PAYPAL_BASE_URL")

    # Set up API endpoints
    base_url = url
    token_url = base_url + '/v1/oauth2/token'
    payment_url = base_url + '/v1/payments/payment'

    # Request an access token
    token_payload = {'grant_type': 'client_credentials'}
    token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
    token_response = requests.post(token_url, auth=(client_id, secret), data=token_payload, headers=token_headers)

    if token_response.status_code != 200:
        raise Exception('Failed to authenticate with PayPal API.')

    access_token = token_response.json()['access_token']

    # Retrieve payment details
    payment_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payment_details_url = f'{payment_url}/{payment_id}'
    payment_details_response = requests.get(payment_details_url, headers=payment_headers)

    if payment_details_response.status_code != 200:
        raise Exception('Failed to retrieve PayPal payment details.')

    payment_status = payment_details_response.json()['state']
    if payment_status == 'approved':
        # Payment is successful, process the order
        # Retrieve additional payment details if needed
        payer_email = payment_details_response.json()['payer']['payer_info']['email']
        # ... process the order ...
        return True
    else:
        # Payment failed or was canceled
        return False
    
def create_subscription(request, id):
    plan = Subscription.objects.get(id=id)

    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/subscription/execute/'),
            "cancel_url": request.build_absolute_uri('/subscription/cancel/')
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": f"{plan.user.username} - {plan.start_date}",
                    "sku": f"plan_{plan.id}",
                    "price": str(plan.amount),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(plan.amount),
                "currency": "USD"
            },
            "description": f"Subscription to {plan.user.username} - {plan.start_date}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                return approval_url
    else:
        return payment.error