from django.contrib import admin

from apps.orders.models.products import ProductImage, Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_uz',)
    search_fields = ('name_uz',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # change_form_template = "admin/orders/product/change_form.html"
    inlines = [ProductImageInline]
