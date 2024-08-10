import logging
from datetime import datetime

import stripe
from rest_framework import serializers

from apps.orders.models.products import ProductImage, Product, Category

logger = logging.getLogger(__name__)

from django.http import HttpRequest


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
                  'category', 'images', 'best_deals', 'stripe_price_id', 'stripe_product_id', 'amount']

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        return [request.build_absolute_uri(image.image.url) for image in images]

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        product = Product.objects.create(**validated_data)

        image_urls = []
        for image in images:
            product_image = ProductImage.objects.create(product=product, image=image)
            image_urls.append(request.build_absolute_uri(product_image.image.url))

        stripe_data = self.create_stripe_product(
            product.name_uz,
            product.description_uz,
            product.price,
            product.amount,
            image_urls
        )
        product.stripe_product_id = stripe_data['product_id']
        product.stripe_price_id = stripe_data['price_id']
        product.save()
        return product

    @staticmethod
    def create_stripe_product(name, description, price, amount, image_urls):
        product = stripe.Product.create(
            name=name,
            description=description,
            images=image_urls,  # Ensure this is a list of absolute URLs
            metadata={
                'amount': str(amount)  # Convert to string
            }
        )

        price_obj = stripe.Price.create(
            product=product.id,
            currency='aed',
            unit_amount=int(price * 100.0),
        )
        return {'product_id': product.id, 'price_id': price_obj.id}

    @staticmethod
    def update_stripe_product(product, request: HttpRequest):
        # Build absolute URLs for images
        image_urls = []
        for image in product.images.all():
            image_url = image.image.url  # This gives the URL relative to MEDIA_URL
            full_image_url = request.build_absolute_uri(image_url).replace('http://', 'https://')
            image_urls.append(full_image_url)

        # Update the Stripe product
        stripe.Product.modify(
            product.stripe_product_id,
            images=image_urls,
            # Other parameters
        )

    @staticmethod
    def delete_stripe_product(product):
        if product.stripe_product_id:
            stripe.Product.modify(
                product.stripe_product_id,
                active=False
            )

    @staticmethod
    def generate_payment_link(order_items):
        try:
            line_items = []
            for item in order_items:
                product = item.product
                if product.amount < item.quantity:
                    return {'error': f'Product {product.name_uz} is out of stock or insufficient quantity available.'}

                line_items.append({
                    'price': product.stripe_price_id,
                    'quantity': item.quantity,
                })

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='https://your-success-url.com/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://your-cancel-url.com/cancel',
            )
            expiration_time = session.expires_at - int(datetime.now().timestamp())
            return {'payment_url': session.url, 'expiration_time': expiration_time}
        except Exception as e:
            return {'error': str(e)}


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image', 'products']



class OnlyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image']
