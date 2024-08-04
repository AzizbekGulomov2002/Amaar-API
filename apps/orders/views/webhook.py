import logging

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from apps.orders.models.orders import Order
from apps.orders.models.payment import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)


@csrf_exempt
def stripe_webhook(request):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    payload = request.body.decode('utf-8')
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        event_type = event['type']
        data_object = event['data']['object']
        logger.info(f"Received event: {event_type}")

        if event_type == 'charge.succeeded':
            charge = data_object
            description = charge.get('description')
            if description:
                try:
                    order_id = description.split(' ')[1]
                    logger.info(f"Order ID from charge: {order_id}")
                    order = Order.objects.get(id=order_id)
                    Payment.objects.create(
                        order=order,
                        stripe_charge_id=charge['id'],
                        amount=charge['amount'] / 100
                    )
                    order.update_status(Order.Status.SHIPPED, Order.PaymentStatus.SUCCEEDED)
                except Order.DoesNotExist:
                    logger.error(f"Order {order_id} does not exist")
            else:
                logger.error("Charge description is missing.")

        elif event_type == 'payment_intent.succeeded':
            payment_intent = data_object
            metadata = payment_intent.get('metadata', {})
            order_id = metadata.get('order_id')

            if order_id:
                try:
                    logger.info(f"Order ID from payment intent: {order_id}")
                    order = Order.objects.get(id=order_id)
                    Payment.objects.create(
                        order=order,
                        stripe_charge_id=payment_intent['id'],
                        amount=payment_intent['amount_received'] / 100
                    )
                    order.update_status(Order.Status.PENDING, Order.PaymentStatus.SUCCEEDED)
                except Order.DoesNotExist:
                    logger.error(f"Order {order_id} does not exist")

            else:

                logger.error("Order ID is missing in payment intent metadata.")

        elif event_type == 'payment_intent.payment_failed':
            payment_intent = data_object
            metadata = payment_intent.get('metadata', {})
            order_id = metadata.get('order_id')
            if order_id:
                try:
                    logger.info(f"Order ID from payment intent: {order_id}")
                    order = Order.objects.get(id=order_id)
                    order.update_status(Order.Status.CANCELED, Order.PaymentStatus.FAILED)
                except Order.DoesNotExist:
                    logger.error(f"Order {order_id} does not exist")
            else:
                logger.error("Order ID is missing in payment intent metadata.")
        return HttpResponse(status=200)

    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return HttpResponse(status=500)
