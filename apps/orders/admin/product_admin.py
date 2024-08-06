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
<<<<<<< HEAD
    # change_form_template = "admin/orders/product/change_form.html"
=======
>>>>>>> 1658386e5903367e192eb855052b738e05580e71
    inlines = [ProductImageInline]
