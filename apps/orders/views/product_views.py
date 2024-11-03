from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.orders.filters import CategoryFilter, ProductFilter
from apps.orders.models.products import Category, Product
from apps.orders.serializers.product_serializer import CategorySerializer, ProductImportSerializer, ProductSerializer,CategoryImportSerializer
from apps.orders.views.base_views import BasePagination
from rest_framework.permissions import IsAuthenticated
import openpyxl
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action


class CategoryViewSet(viewsets.ModelViewSet):
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CategoryFilter
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = []
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    pagination_class = BasePagination
    search_fields = ['name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en']

    TRANSLATIONS = {
        'success': {
            'ru': 'Успешно',
            'en': 'Success',
        },
        'error': {
            'ru': 'Ошибка',
            'en': 'Error',
        },
    }

    def get_translated_message(self, key, lang='en'):
        return self.TRANSLATIONS.get(key, {}).get(lang, key)

    @action(detail=False, methods=['get'], url_path='by-ids')
    def get_products_by_ids(self, request, *args, **kwargs):
        ids = request.query_params.get('ids', None)
        if ids:
            ids_list = ids.split(',')
            queryset = self.get_queryset().filter(id__in=ids_list)
        else:
            queryset = self.get_queryset().none()

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context={'request': request})

        # Generate the message dictionary for multiple languages
        message = {
            'ru': self.get_translated_message('success', 'ru'),
            'en': self.get_translated_message('success', 'en'),
        }

        return self.get_paginated_response({
            'message': message,
            'data': serializer.data
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True, context={'request': request})

        # Generate the message dictionary for multiple languages
        message = {
            'ru': self.get_translated_message('success', 'ru'),
            'en': self.get_translated_message('success', 'en'),
        }

        return self.get_paginated_response({
            'message': message,
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound:
            message = {
                'ru': self.get_translated_message('error', 'ru'),
                'en': self.get_translated_message('error', 'en'),
            }
            return Response({
                'count': 0,
                'next': None,
                'previous': None,
                'results': {
                    'message': message,
                    'data': []
                }
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        message = {
            'ru': self.get_translated_message('success', 'ru'),
            'en': self.get_translated_message('success', 'en'),
        }

        return Response({
            'count': 1,
            'next': None,
            'previous': None,
            'results': {
                'message': message,
                'data': [serializer.data]  # Wrap in a list for consistency
            }
        })


class ProductImportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProductImportSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()  # Call the create method
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryImportView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request, *args, **kwargs):
        serializer = CategoryImportSerializer(data=request.data)
        if serializer.is_valid():
            # Call the import method to process the uploaded file
            count = serializer.import_categories()
            return Response({'message': f'Successfully imported {count} categories.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class BestProductsListView(generics.ListAPIView):
    queryset = Product.objects.filter(best_deals=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer

class AllCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CategoryFilter

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset
