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
from apps.orders.serializers.product_serializer import CategorySerializer, ProductImportSerializer, ProductSerializer
from apps.orders.views.base_views import BasePagination


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
        file = request.FILES.get('file')

        if not file or not file.name.endswith('.xlsx'):
            return Response({'error': 'Please upload a valid Excel file (.xlsx)'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            wb = load_workbook(file, data_only=True)
            ws = wb.active
        except Exception as e:
            return Response({'error': 'Failed to process the Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

        products = []
        errors = []
        
        for idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            name_uz = row[0]
            name_ru = row[1]
            name_en = row[2]
            price = row[3]
            quantity = row[4]
            category_uz = row[5]
            category_ru = row[6]
            category_en = row[7]
            best_deals = row[8]

            product_data = {
                'name_uz': name_uz,
                'name_ru': name_ru,
                'name_en': name_en,
                'price': price,
                'quantity': quantity,
                'category_uz': category_uz,
                'category_ru': category_ru,
                'category_en': category_en,
                'best_deals': bool(best_deals),
            }

            serializer = ProductImportSerializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
                products.append(serializer.data)
            else:
                errors.append({'row': idx, 'errors': serializer.errors})

        if errors:
            return Response({'error': 'Some rows had errors', 'details': errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Products imported successfully', 'products': products}, status=status.HTTP_201_CREATED)




class BestProductsListView(generics.ListAPIView):
    queryset = Product.objects.filter(best_deals=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
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
