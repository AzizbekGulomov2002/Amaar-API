from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from apps.orders.models.orders import OrderHistory, Order
from apps.orders.serializers.order_serializer import OrderHistoryIDSerializer, OrderHistoryBaseSerializers, \
    OrderSerializer


class OrderHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-id')
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Debug log to check order items
        order_items = serializer.validated_data.get('order_items', [])
        for item in order_items:
            print(f"Product ID: {item.product.id}, Price: {item.product.price}")

        order_data = serializer.save()
        return Response(order_data, status=status.HTTP_201_CREATED)


class UpdateDeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        delivery_status = request.data.get('delivery_status')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        if order.type_order != 'cash':
            return Response({'error': 'This endpoint is only for cash payments'}, status=status.HTTP_400_BAD_REQUEST)

        if delivery_status == 'delivered':
            order.order_status = 'delivered'
            order.payment_status = 'succeeded'
        elif delivery_status == 'canceled':
            order.order_status = 'canceled'
            order.payment_status = 'canceled'
        else:
            return Response({'error': 'Invalid delivery status'}, status=status.HTTP_400_BAD_REQUEST)

        order.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
