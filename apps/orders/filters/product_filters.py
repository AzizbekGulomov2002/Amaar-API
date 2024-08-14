import django_filters

from apps.orders.models import Category, Product


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = ['name_ru', 'name_en']


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name_uz', 'name_ru', 'name_en']
