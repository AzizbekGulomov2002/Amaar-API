from datetime import datetime

import stripe
from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models.orders import Order
from apps.orders.models.payment import Payment
from apps.orders.serializers.product_serializer import ProductSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.type_order == 'cash':
            return Response({'error': 'Payment link cannot be generated for cash payments'},
                            status=status.HTTP_400_BAD_REQUEST)

        products = order.products.all()
        for item in products:
            if item.product.quantity < item.quantity:
                return Response({'error': f"Insufficient quantity for product {item.product.name_uz}"},
                                status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'payment_link_{order_id}'
        cache_data = cache.get(cache_key)

        if cache_data:
            remaining_time = cache_data['expires_in'] - int(datetime.now().timestamp() - cache_data['created_at'])
            if cache_data['access_count'] < 3:
                cache_data['access_count'] += 1
                cache.set(cache_key, cache_data, timeout=3600)
                remaining_attempts = 3 - cache_data['access_count']
                return Response({
                    'payment_url': cache_data['payment_link'],
                    'expires_in': max(remaining_time, 0),
                    'remaining_attempts': remaining_attempts
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Too many tries, try again after one hour.',
                    'retry_after_seconds': max(remaining_time, 0)
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            payment_link_data = ProductSerializer.generate_payment_link(products)

            if "error" in payment_link_data:
                return Response(payment_link_data, status=status.HTTP_400_BAD_REQUEST)

            expires_in = 3600
            cache_data = {
                'payment_link': payment_link_data['payment_url'],
                'session_id': payment_link_data['session_id'],
                'access_count': 1,
                'expires_in': expires_in,
                'created_at': int(datetime.now().timestamp()),
            }

            cache.set(cache_key, cache_data, timeout=expires_in)
            for item in products:
                Payment.objects.create(
                    product=item.product,
                    order=order,
                    price=item.product.price,
                    quantity=item.quantity,
                    stripe_session_id=payment_link_data['session_id'],
                    status='pending'
                )
            return Response({
                'payment_url': payment_link_data['payment_url'],
                'expires_in': expires_in,
                'remaining_attempts': 3,
                'created_at': int(datetime.now().timestamp())
            }, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
