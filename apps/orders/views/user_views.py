from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from apps.orders.models.orders import Order
from apps.orders.serializers.order_serializer import OrderSerializer


class UserOrderHistoryAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        orders_serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(orders_serializer.data)
