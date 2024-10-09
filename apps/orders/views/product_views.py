from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl import load_workbook
from rest_framework import status
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.orders.filters import CategoryFilter, ProductFilter
from apps.orders.models.products import Category, Product
from apps.orders.serializers.product_serializer import CategorySerializer, ProductImportSerializer, ProductSerializer,CategoryImportSerializer
from apps.orders.views.base_views import BasePagination
from rest_framework.permissions import IsAuthenticated


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

class ProductImportView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = ProductImportSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryImportView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CategoryImportSerializer(data=request.data)
        if serializer.is_valid():
            created_count = serializer.import_categories()
            return Response({'message': f'{created_count} categories imported successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BestProductsListView(generics.ListAPIView):
    queryset = Product.objects.filter(best_deals=True)
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

class AllCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CategoryFilter

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset
