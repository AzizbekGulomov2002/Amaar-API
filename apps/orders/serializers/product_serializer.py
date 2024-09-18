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
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'price',
                  'category_ru','category_en', 'images', 'best_deals', 'quantity', 'created_at', 'uploaded_images','show_main_page']

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
            images = [request.build_absolute_uri(image.image.url) for image in product.product_images.all()]
            line_items.append({
                'price_data': {
                    'currency': 'aed',
                    'product_data': {
                        'name': product.name_uz,
                        'description': product.description_uz,
                        'images': images,
                    },
                    'unit_amount': int(product.price * 100),
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

# class ProductImportSerializer(serializers.ModelSerializer):
#     category_uz = serializers.CharField(max_length=255, allow_blank=True, required=False, allow_null=True)
#     category_ru = serializers.CharField(max_length=255, allow_blank=True, required=False, allow_null=True)
#     category_en = serializers.CharField(max_length=255, allow_blank=True, required=False, allow_null=True)
#     price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
#     description_uz = serializers.CharField(max_length=255, allow_blank=True, required=False, allow_null=True)
#     description_ru = serializers.CharField(max_length=255, allow_blank=True, required=False, allow_null=True)
#     description_en = serializers.CharField(max_length=255, allow_blank=True, required=False, allow_null=True)

#     class Meta:
#         model = Product
#         fields = ['name_uz', 'name_ru', 'name_en', 'price', 'quantity', 'category_uz', 'category_ru', 'category_en', 'best_deals', 'description_uz', 'description_ru', 'description_en']

#     def create(self, validated_data):
#         # Extract category names
#         category_uz_name = validated_data.pop('category_uz', None)
#         category_ru_name = validated_data.pop('category_ru', None)
#         category_en_name = validated_data.pop('category_en', None)

#         # Fetch or create the related categories
#         category_uz = None
#         if category_uz_name:
#             category_uz, _ = Category.objects.get_or_create(name_uz=category_uz_name)
        
#         category_ru = None
#         if category_ru_name:
#             category_ru, _ = Category.objects.get_or_create(name_ru=category_ru_name)
        
#         category_en = None
#         if category_en_name:
#             category_en, _ = Category.objects.get_or_create(name_en=category_en_name)

#         # Create the product with the fetched or created categories
#         product = Product.objects.create(
#             **validated_data,
#             category_uz=category_uz,
#             category_ru=category_ru,
#             category_en=category_en,  # Include category_en here
#         )

#         return product

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Category
        fields = ['id', "name_uz", 'name_ru', 'name_en', 'image', 'products']


class ProductImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        file = validated_data.get('file')
        workbook = load_workbook(file, data_only=True)
        sheet = workbook.active
        
        # Iterate through the rows, assuming the first row is the header
        products = []
        for row in sheet.iter_rows(min_row=2, values_only=True):  # Start from the second row
            name_uz = row[0]
            name_ru = row[1]
            name_en = row[2]
            description_uz = row[3]
            description_ru = row[4]
            description_en = row[5]
            price = row[6]
            quantity = row[7]
            category_uz_name = row[8]
            category_ru_name = row[9]
            category_en_name = row[10]
            best_deals = row[11] == "Yes"
            
            # Get or create categories for each language
            category_uz = Category.objects.filter(name_uz=category_uz_name).first()
            category_ru = Category.objects.filter(name_ru=category_ru_name).first()
            category_en = Category.objects.filter(name_en=category_en_name).first()
            
            if not (category_uz and category_ru and category_en):
                continue  # If any category is missing, skip this product

            # Create a new product
            product = Product(
                name_uz=name_uz,
                name_ru=name_ru,
                name_en=name_en,
                description_uz=description_uz,
                description_ru=description_ru,
                description_en=description_en,
                price=price,
                quantity=quantity,
                category_uz=category_uz,
                category_ru=category_ru,
                category_en=category_en,
                best_deals=best_deals,
            )
            products.append(product)
        
        # Bulk create products
        Product.objects.bulk_create(products)
        return {'imported': len(products)}

class CategoryImportSerializer(serializers.Serializer):
    file = serializers.FileField()

    def import_categories(self):
        file = self.validated_data['file']
        wb = openpyxl.load_workbook(file)
        ws = wb.active

        categories = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            category_data = {
                'name_uz': row[0],
                'name_ru': row[1],
                'name_en': row[2],
            }
            categories.append(Category(**category_data))

        Category.objects.bulk_create(categories)
        return len(categories)

class OnlyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', "name_uz", 'name_ru', 'name_en', 'image']
