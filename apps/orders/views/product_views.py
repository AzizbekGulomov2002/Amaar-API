from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.db import transaction
from openpyxl import load_workbook
from rest_framework.views import APIView
from rest_framework import status

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en']



class ProductImportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        company_id = request.user.company_id
        serializer = ProductImportSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                workbook = load_workbook(filename=file, read_only=True)
                sheet = workbook.active
                imported_products = []

                with transaction.atomic():
                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        if not row or len(row) < 10:  # Ensure all columns are present
                            continue
                        
                        category_name, price, quantity, name_uz, name_ru, name_en, description_uz, description_ru, description_en = row[:9]

                        if Product.objects.filter(name_uz=name_uz, company_id=company_id).exists():
                            return Response({
                                "error": {
                                    "uz": f"'{name_uz}' nomli mahsulot allaqachon mavjud",
                                    "ru": f"Продукт с названием '{name_uz}' уже существует",
                                    "en": f"Product named '{name_uz}' already exists"
                                }
                            }, status=status.HTTP_400_BAD_REQUEST)

                        # Check if category exists
                        category = Category.objects.filter(name=category_name, company_id=company_id).first()
                        if not category:
                            return Response({
                                "error": {
                                    "uz": f"Kategoriya '{category_name}' mavjud emas",
                                    "ru": f"Категория '{category_name}' не существует",
                                    "en": f"Category '{category_name}' does not exist"
                                }
                            }, status=status.HTTP_400_BAD_REQUEST)

                        # Create product
                        product = Product.objects.create(
                            company_id=company_id,
                            category=category,
                            price=price,
                            quantity=quantity,
                            name_uz=name_uz,
                            name_ru=name_ru,
                            name_en=name_en,
                            description_uz=description_uz,
                            description_ru=description_ru,
                            description_en=description_en,
                        )

                        imported_products.append(ProductSerializer(product).data)

                return Response({
                    "success": {
                        "uz": "Mahsulotlar muvaffaqiyatli import qilindi",
                        "ru": "Продукты успешно импортированы",
                        "en": "Products were successfully imported"
                    },
                    "products": imported_products
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({
                    "error": {
                        "uz": f"Xatolik yuz berdi: {str(e)}",
                        "ru": f"Произошла ошибка: {str(e)}",
                        "en": f"An error occurred: {str(e)}"
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "errors": serializer.errors,
            "message": {
                "uz": "Noto'g'ri ma'lumotlar kiritildi. Iltimos, kiritgan ma'lumotlaringizni tekshiring.",
                "ru": "Предоставлены неверные данные. Пожалуйста, проверьте ваш ввод.",
                "en": "Invalid data provided. Please check your input."
            }
        }, status=status.HTTP_400_BAD_REQUEST)



class BestProductsListView(generics.ListAPIView):
    queryset = Product.objects.filter(best_deals=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer


class AllCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CategoryFilter

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset
