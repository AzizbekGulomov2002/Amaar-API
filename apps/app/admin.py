from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')
    search_fields = ('address',)
    inlines = [OrderItemInline]


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['order__id', 'user__username']

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_filter = ('order__address', 'product')

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name_uz', 'price', 'category')
#     list_filter = ('category',)
#     search_fields = ('name_uz',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)


# Register Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uz',)
    search_fields = ('name_uz',)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('color', 'product')
    search_fields = ('color', 'product__name_uz')
    # Additional configurations as needed


@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')

@admin.register(PolicyAndPrivacy)
class PolicyAndPrivacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')

@admin.register(PublicOffer)
class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')

@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')