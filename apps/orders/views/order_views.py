from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.orders.models.orders import OrderHistory, Order
from apps.orders.serializers.order_serializer import OrderHistoryIDSerializer, OrderHistoryBaseSerializers, \
    OrderSerializer


class OrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderHistory.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderHistoryIDSerializer
        return OrderHistoryBaseSerializers

    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        order_history = self.get_object()
        serializer = OrderHistoryBaseSerializers(order_history)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def all_orders(self, request):
        order_histories = OrderHistory.objects.all()
        serializer = OrderHistoryBaseSerializers(order_histories, many=True)
        return Response(serializer.data)


class OrderListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-id')
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-id')
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def create_payment_session(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order)
        payment_data = serializer.generate_payment_link(serializer.validated_data['products'])
        if 'error' in payment_data:
            return Response({'detail': payment_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(payment_data, status=status.HTTP_200_OK)
