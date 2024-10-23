from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.orders.models.products import Product, ProductImage, Category


# Define an inline admin for ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    can_delete = True
    show_change_link = True


# Define the admin for the Product model
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en', 'price', 'quantity', 'category', 'best_deals', 'show_main_page', 'created_at')
    list_filter = ('category', 'best_deals', 'show_main_page')
    search_fields = ('name_uz', 'name_ru', 'name_en', 'price')
    ordering = ['name_uz']
    readonly_fields = ('created_at',)
    # list_per_page = 10
    inlines = [ProductImageInline]

# Register the Product model with the admin site
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name_uz', 'name_ru', 'name_en', 'created_at')
    search_fields = ('name_uz', 'name_ru', 'name_en')
    ordering = ['name_ru', 'name_en']
    readonly_fields = ('created_at',)
    list_per_page = 10
admin.site.register(Category, CategoryAdmin)



