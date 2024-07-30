from django.db.models import Count
from django.utils.timezone import now
from rest_framework import viewsets, generics, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import stripe
from .models import *
from .serializers import *
from ..users.models import User
from django.utils.timezone import now
from datetime import timedelta, date, datetime
from rest_framework.pagination import BasePagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from apps.app.filters import CategoryFilter, ProductFilter
from rest_framework.decorators import action
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = int(order.total_quantity * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description=f'Order {order_id}',
                source=request.data.get('stripe_token')
            )
            payment = Payment.objects.create(
                order=order,
                stripe_charge_id=charge['id'],
                amount=order.total_quantity
            )
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if event['type'] == 'charge.succeeded':
            charge = event['data']['object']
            order_id = charge['description'].split(' ')[1]
            order = Order.objects.get(id=order_id)
            Payment.objects.create(
                order=order,
                stripe_charge_id=charge['id'],
                amount=charge['amount'] / 100  # Convert cents to dollars
            )

        return Response(status=status.HTTP_200_OK)

class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            "current": self.page.number,
            "pageSize": self.page.paginator.per_page,
            "total": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })

class CustomPaginationMixin:
    pagination_class = BasePagination

class AllCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CategoryFilter
    ordering_fields = ['name']
    search_fields = ['name']

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CategoryFilter
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductFilter
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    search_fields = ['name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en']


class BestProductsListView(generics.ListAPIView):
    queryset = Product.objects.filter(best_deals=True)
    serializer_class = ProductSerializer


class DeliveryInfoViewSet(viewsets.ModelViewSet):
    queryset = DeliveryInfo.objects.all()
    serializer_class = DeliveryInfoSerializer


class PolicyAndPrivacyViewSet(viewsets.ModelViewSet):
    queryset = PolicyAndPrivacy.objects.all()
    serializer_class = PolicyAndPrivacySerializer


class PublicOfferViewSet(viewsets.ModelViewSet):
    queryset = PublicOffer.objects.all()
    serializer_class = PublicOfferSerializer


class ReturnPolicyViewSet(viewsets.ModelViewSet):
    queryset = ReturnPolicy.objects.all()
    serializer_class = ReturnPolicySerializer

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all().order_by('-id')
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticated]




class UserOrderHistoryAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Order.objects.filter(user_id=user_id).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        orders_serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(orders_serializer.data)
    


class OrderHistoryBaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['id', 'order', 'user', 'date', 'status']

    def create(self, validated_data):
        order_history = super().create(validated_data)
        # Update the order status
        order = order_history.order
        order.status = order_history.status
        order.save()
        return order_history

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # Update the order status
        order = instance.order
        order.status = instance.status
        order.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation


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


# class PaymentLinkViewSet(generics.GenericAPIView):
#     serializer_class = GeneratePaymentLinkSerializer
#     def post(self, request, *args, **kwargs):
#         order_id = request.data.get("order_id")
#         order_id.objects.get(Order)



class PaymentLinkViewSet(generics.GenericAPIView):
    serializer_class = GeneratePaymentLinkSerializer
    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        if not order_id:
            return Response({"error":"order id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        payment_link = self.generate_payment_link(order)
        return Response({"payment_link":payment_link}, status=status.HTTP_200_OK)



class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        total_orders = Order.objects.count()
        total_users = User.objects.count()
        users_for_this_month = User.objects.filter(date_joined__gte=start_of_month).count()
        users_for_this_week = User.objects.filter(date_joined__gte=start_of_week).count()
        users_for_today = User.objects.filter(date_joined__date=today).count()
        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_banner = Banner.objects.count()

        orders_by_day = Order.objects.extra(select={'day': 'date(created_at)'}).values('day').annotate(count=Count('id')).order_by('day')
        top_products = OrderItem.objects.values('product__id').annotate(count=Count('id')).order_by('-count')[:10]
        top_users = Order.objects.values('user__id').annotate(count=Count('id')).order_by('-count')[:10]
        top_categories = Product.objects.values('category__id').annotate(count=Count('id')).order_by('-count')[:10]

        # Ensure datetime objects are converted to ISO format strings
        for order in orders_by_day:
            order['day'] = order['day'].isoformat() if isinstance(order['day'], (date, datetime)) else order['day']

        data = {
            "total_orders": total_orders,
            "total_users": total_users,
            "users_for_this_month": users_for_this_month,
            "users_for_this_week": users_for_this_week,
            "users_for_today": users_for_today,
            "total_products": total_products,
            "total_categories": total_categories,
            "total_banner": total_banner,
            "orders_by_day": list(orders_by_day),
            "top_products": list(top_products),
            "top_users": list(top_users),
            "top_categories": list(top_categories)
        }

        serializer = DashboardSerializer(data)
        return Response(serializer.data)
