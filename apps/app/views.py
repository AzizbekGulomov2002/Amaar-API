from django.db.models import Count
from django.utils.timezone import now
from rest_framework import viewsets, generics, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *
from ..users.models import User
from django.utils.timezone import now
from datetime import timedelta, date, datetime
from rest_framework.pagination import BasePagination, PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from apps.app.filters import CategoryFilter, ProductFilter


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


# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all().order_by('-id')
#     serializer_class = CategorySerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = BasePagination
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
#     filterset_class = CategoryFilter
#     ordering_fields = ['name']
#     search_fields = ['name']
#     basename = 'category'
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#

#
class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CategoryFilter
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProductFilter
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en']
    # ordering = ['-id']






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
