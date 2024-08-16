from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from apps.orders.filters import CategoryFilter, ProductFilter
from apps.orders.models.products import Category, Product
from apps.orders.serializers.product_serializer import CategorySerializer, ProductSerializer
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
