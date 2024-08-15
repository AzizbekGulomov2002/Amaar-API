import time
from datetime import datetime

import stripe
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import serializers

from apps.orders.models.products import ProductImage, Product, Category


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'image_url']
        extra_kwargs = {
            'product': {'write_only': True},
            'image': {'write_only': True},
        }

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'price',
                  'category', 'images', 'best_deals', 'quantity', 'created_at', 'uploaded_images']

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
            product_description = product.description_uz

            line_items.append({
                'price_data': {
                    'currency': 'aed',
                    'product_data': {
                        'name': product.name_uz,
                        'description': product_description,
                        'images': images,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': item.quantity,
            })

        base_url = request.build_absolute_uri('/')
        success_url = base_url + reverse('payment_success')
        cancel_url = base_url + reverse('payment_fail')

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


class OnlyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', "name_uz", 'name_ru', 'name_en', 'image']
