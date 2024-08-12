import logging

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from apps.orders.models.payment import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body.decode('utf-8')
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    logger.info(f"Received webhook: {payload}")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        logger.info(f"Webhook event: {event}")
    except ValueError as e:
        logger.error(f"Webhook error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Signature verification error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

    event_type = event['type']
    logger.info(f"Handling event type: {event_type}")

    if event_type == 'checkout.session.completed':
        session = event['data']['object']
        handle_payment_status(session['id'], 'succeeded')
    elif event_type in ['checkout.session.async_payment_failed', 'payment_intent.payment_failed']:
        session = event['data']['object']
        handle_payment_status(session['id'], 'failed')
    elif event_type == 'payment_intent.canceled':
        session = event['data']['object']
        handle_payment_status(session['id'], 'canceled')
    elif event_type == 'payment_intent.expired':
        session = event['data']['object']
        handle_payment_status(session['id'], 'expired')

    return JsonResponse({'status': 'success'}, status=200)


def handle_payment_status(session_id, status):
    try:
        payments = Payment.objects.filter(stripe_session_id=session_id)
        for payment in payments:
            payment.status = status
            payment.save()
            order = payment.order
            order.payment_status = status

            if status == 'succeeded':
                order.order_status = 'success'
                product = payment.product
                product.quantity -= payment.quantity
                product.save()
            elif status in ['failed', 'canceled', 'expired']:
                order.order_status = 'canceled'
                product = payment.product
                product.quantity += payment.quantity
                product.save()

            order.save()
    except Payment.DoesNotExist:
        logger.error(f"No payments found with session_id: {session_id}")
