import stripe
from django.conf import settings
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models.orders import Order
from apps.orders.serializers.payment_serializer import GeneratePaymentLinkSerializer
from apps.orders.serializers.product_serializer import ProductSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        products = order.products.all()
        for order_item in products:
            if order_item.product.amount <= 0:
                return Response({'error': f'Product {order_item.product.name_uz} is out of stock.'},
                                status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'payment_link_{order_id}'
        cache_data = cache.get(cache_key)

        if cache_data:
            remaining_time = cache.ttl(cache_key)
            if cache_data['access_count'] < 3:
                cache_data['access_count'] += 1
                cache.set(cache_key, cache_data, timeout=remaining_time)
                remaining_attempts = 3 - cache_data['access_count']
                return Response({
                    'payment_url': cache_data['payment_link'],
                    'expires_in': remaining_time,
                    'remaining_attempts': remaining_attempts
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Too many tries, try again after one hour.',
                    'retry_after_seconds': remaining_time
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        try:
            payment_link_data = ProductSerializer.generate_payment_link(products)

            if "error" in payment_link_data:
                return Response(payment_link_data, status=status.HTTP_400_BAD_REQUEST)

            expires_in = payment_link_data['expiration_time']
            cache.set(cache_key, {
                'payment_link': payment_link_data['payment_url'],
                'access_count': 1,
                'expires_in': expires_in
            }, timeout=3600)
            order.update_status(Order.Status.PENDING, Order.PaymentStatus.PENDING)
            return Response({
                'payment_url': payment_link_data['payment_url'],
                'expires_in': expires_in,
                'remaining_attempts': 2
            }, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentLinkViewSet(generics.GenericAPIView):
    serializer_class = GeneratePaymentLinkSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get("order_id")
        amount = serializer.validated_data.get("amount")

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        product = order.product

        try:
            payment_link = ProductSerializer.generate_payment_link(product, amount)
            return Response({"url": {payment_link}}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
