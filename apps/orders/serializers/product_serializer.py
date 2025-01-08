import time
from datetime import datetime
import openpyxl
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import serializers
from openpyxl import load_workbook

from apps.orders.models.products import ProductImage, Product, Category


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True, source='product_images')
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'price','category', 'images', 'best_deals', 'quantity', 'created_at', 'uploaded_images','show_main_page']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product

    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = super().update(instance, validated_data)

        if uploaded_images:
            ProductImage.objects.filter(product=product).delete()
            for image in uploaded_images:
                ProductImage.objects.create(product=product, image=image)
        return product

    @staticmethod
    def generate_payment_link(order_items, request):
        line_items = []
        for item in order_items:
            product = item.product

            # Check if price is None
            if product.price is None:
                raise ValueError(f"Product {product.id} has no price set.")

            images = [request.build_absolute_uri(image.image.url) for image in product.product_images.all()]
            
            # Set default description if empty
            description = product.description_uz if product.description_uz else "No description available"

            line_items.append({
                'price_data': {
                    'currency': 'aed',
                    'product_data': {
                        'name': product.name_uz,
                        'description': description,
                        'images': images,
                    },
                    'unit_amount': int(product.price * 100),  # Assuming product.price is now guaranteed to be a valid number
                },
                'quantity': item.quantity,
            })

        success_url = request.build_absolute_uri(reverse('payment_success'))
        cancel_url = request.build_absolute_uri(reverse('payment_fail'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{success_url}?{urlencode({"session_id": "{CHECKOUT_SESSION_ID}"})}',
            cancel_url=cancel_url,
            expires_at=int(time.time() + 3600),
        )

        expiration_time = session.expires_at - int(datetime.now().timestamp())
        return {
            'payment_url': session.url,
            'expiration_time': expiration_time,
            'session_id': session.id
        }





class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Category
        fields = ['id', "name_uz", 'name_ru', 'name_en', 'image', 'products']


# class ProductImportSerializer(serializers.Serializer):
#     file = serializers.FileField()

#     def create(self, validated_data):
#         file = validated_data.get('file')
#         workbook = load_workbook(file, data_only=True)
#         sheet = workbook.active
        
#         products = []
#         errors = []

#         for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):  # Start from the second row
#             # Extract values from the row
#             category_id = row[0]  # Assuming category_id is in the first column
#             name_uz = row[1]      # Name in Uzbek
#             name_ru = row[2]      # Name in Russian
#             name_en = row[3]      # Name in English
#             price = row[4]        # Price
#             quantity = row[5]     # Quantity
#             description_uz = row[6] if len(row) > 6 else None  # Optional description in Uzbek
#             description_ru = row[7] if len(row) > 7 else None  # Optional description in Russian
#             description_en = row[8] if len(row) > 8 else None  # Optional description in English
            
#             # Validate category_id
#             category = Category.objects.filter(id=category_id).first()
#             if not category:
#                 errors.append({"row": row_index + 2, "error": f"Category ID '{category_id}' not found."})
#                 continue  # Skip this product if the category is missing

#             # Create a new product instance
#             product = Product(
#                 category=category,
#                 name_uz=name_uz,
#                 name_ru=name_ru,
#                 name_en=name_en,
#                 price=price,
#                 quantity=quantity,
#                 description_uz=description_uz,
#                 description_ru=description_ru,
#                 description_en=description_en,
#             )
#             products.append(product)
        
#         # Bulk create products
#         if products:
#             Product.objects.bulk_create(products)

#         return {
#             'imported': len(products),
#             'errors': errors
#         }


class ProductImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        file = validated_data.get('file')
        workbook = load_workbook(file, data_only=True)
        sheet = workbook.active

        products = []
        errors = []

        for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):  # Start from the second row
            # Extract and validate fields
            category_id = row[0]
            name_uz = row[1]  # Optional
            name_ru = row[2]  # Optional
            name_en = row[3]  # Optional
            price = row[4]  # Optional
            quantity = row[5]  # Optional
            description_uz = row[6] if len(row) > 6 else None  # Optional
            description_ru = row[7] if len(row) > 7 else None  # Optional
            description_en = row[8] if len(row) > 8 else None  # Optional
            
            # Initialize error tracking for the current row
            row_errors = {"row": row_index + 2, "errors": []}

            # Validate category_id
            if not category_id:
                row_errors["errors"].append("Category ID is required.")
            else:
                category = Category.objects.filter(id=category_id).first()
                if not category:
                    row_errors["errors"].append(f"Category ID '{category_id}' not found.")
            
            # No validation required for name_uz, name_ru, and name_en (all optional now)

            # Validate price (optional, should be positive if provided)
            if price is not None:
                try:
                    price = float(price)
                    if price < 0:
                        row_errors["errors"].append(f"Price must be a positive number, got '{price}'.")
                        price = None  # Set price to None if it's negative
                except (TypeError, ValueError):
                    row_errors["errors"].append(f"Invalid price value, got '{price}'.")
                    price = None  # Set price to None if it's invalid

            # Validate quantity (optional, support both float and int, must be non-negative if provided)
            if quantity is not None:
                try:
                    quantity = int(float(quantity))  # Convert to float first, then cast to int
                    if quantity < 0:
                        row_errors["errors"].append(f"Quantity must be a non-negative integer, got '{quantity}'.")
                        quantity = None
                except (TypeError, ValueError):
                    row_errors["errors"].append(f"Invalid quantity value, got '{quantity}'.")

            # If there are validation errors, add them to the list and skip the row
            if row_errors["errors"]:
                errors.append(row_errors)
                continue

            # If validation passes, create the product instance
            product = Product(
                category=category,
                name_uz=name_uz,  # Can be None
                name_ru=name_ru,  # Can be None
                name_en=name_en,  # Can be None
                price=price,  # Can be None
                quantity=quantity,  # Can be None
                description_uz=description_uz,  # Optional
                description_ru=description_ru,  # Optional
                description_en=description_en   # Optional
            )
            products.append(product)

        # Bulk create products if there are no errors
        if products:
            Product.objects.bulk_create(products)

        return {
            'imported': len(products),
            'errors': errors
        }


class CategoryImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def import_categories(self):
        file = self.validated_data['file']
        wb = openpyxl.load_workbook(file)
        ws = wb.active

        categories = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            name_uz, name_ru, name_en = row  # Unpack the row to get all language fields
            category_data = {
                'name_uz': name_uz,
                'name_ru': name_ru,
                'name_en': name_en,
            }
            # Create a Category instance without saving it to the database yet
            categories.append(Category(**category_data))

        # Use bulk_create for performance reasons
        Category.objects.bulk_create(categories)
        return len(categories)





class OnlyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', "name_uz", 'name_ru', 'name_en', 'image']
