from django.contrib import admin
from .models import Category, Product, Banner, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'latitude', 'longitude')
    search_fields = ('address',)
    inlines = [OrderItemInline]

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order__address', 'product__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register Banner model
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'product')
    search_fields = ('title', 'product__name')
    # Additional configurations as needed