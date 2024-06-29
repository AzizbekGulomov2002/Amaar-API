from django.db.models import Count
from django.utils.timezone import now
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Banner, Category, Product, Order, OrderItem
from .serializers import BannerSerializer, CategorySerializer, ProductSerializer, OrderSerializer, DashboardSerializer
from ..users.models import User
from django.utils.timezone import now
from datetime import timedelta, date, datetime


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]


class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class DashboardView(APIView):
    permission_classes = [AllowAny]

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