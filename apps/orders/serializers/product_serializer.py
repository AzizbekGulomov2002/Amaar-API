import time
from datetime import datetime

import stripe
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
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'description_uz', 'description_ru', 'description_en', 'price',
                  'category', 'images', 'best_deals', 'quantity', 'created_at']

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.product_images.all()
        return [request.build_absolute_uri(image.image.url) for image in images]

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        product = Product.objects.create(**validated_data)

        for image in images:
            ProductImage.objects.create(product=product, image=image)
        product.save()
        return product

    @staticmethod
    def generate_payment_link(order_items):

        line_items = []
        for item in order_items:
            product = item.product
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name_uz,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': item.quantity,
            })

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
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
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image', 'products']
