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
    # ordering = ['-id']


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


class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        return OrderHistory.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)
    


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


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
