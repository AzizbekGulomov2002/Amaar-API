# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

import stripe

from flask import Flask, jsonify, request

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_..."

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_64b556bb62845a1f2fb421940e09b77e0dece0b49d898df0848963fff8e065fc'

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'checkout.session.async_payment_failed':
        session = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
    elif event['type'] == 'checkout.session.completed':
        session = event['data']['object']
    elif event['type'] == 'checkout.session.expired':
        session = event['data']['object']
    elif event['type'] == 'payment_intent.amount_capturable_updated':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.canceled':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.created':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.partially_funded':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.processing':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.requires_action':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
    elif event['type'] == 'payment_link.created':
        payment_link = event['data']['object']
    elif event['type'] == 'payment_link.updated':
        payment_link = event['data']['object']
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']
    elif event['type'] == 'payment_method.automatically_updated':
        payment_method = event['data']['object']
    elif event['type'] == 'payment_method.detached':
        payment_method = event['data']['object']
    elif event['type'] == 'payment_method.updated':
        payment_method = event['data']['object']
    elif event['type'] == 'refund.created':
        refund = event['data']['object']
    elif event['type'] == 'refund.updated':
        refund = event['data']['object']
    # ... handle other event types
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)
