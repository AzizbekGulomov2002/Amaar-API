import stripe
from django.http import JsonResponse
from rest_framework import serializers

from apps.app.models import *
from apps.users.serializers import UserSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

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
                  'category', 'images', 'best_deals', 'stripe_price_id']

    def get_images(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        return [request.build_absolute_uri(image.image.url) for image in images]

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        product = Product.objects.create(**validated_data)
        price_id = self.create_stripe_product(product.name_uz, product.description_uz, product.price)
        product.stripe_price_id = price_id
        product.save()
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product

    @staticmethod
    def create_stripe_product(name, description, price):
        product = stripe.Product.create(
            name=name,
            description=description
        )
        price = stripe.Price.create(
            product=product.get("id"),
            currency='aed',
            unit_amount=int(price * 100.0),
        )
        return price.get("id")

    @staticmethod
    def generate_payment_link(product, amount):
        if product.stripe_price_id:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': product.stripe_price_id,
                    'quantity': amount,
                }],
                mode='payment',
                success_url='https://your-success-url.com/success',
                cancel_url='https://your-success-url.com/cancel',
            )
        else:
            return JsonResponse({"error": "Product has no StripePriceId"}, status=400)

        return session.url


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True, source='product_set')

    class Meta:
        model = Category
        fields = ['id', 'name_uz', 'name_ru', 'name_en', 'image', 'products']


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'color', 'description_uz', 'description_ru', 'description_en', 'image', 'product']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'address', 'latitude', 'longitude', 'comment', 'products', 'user', 'created_at', 'status']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        user = validated_data.pop('user')
        order = Order.objects.create(user=user, **validated_data)
        for product_data in products_data:
            OrderItem.objects.create(order=order, **product_data)
        return order

    def to_representation(self, instance):
        request = self.context.get('request')
        representation = super().to_representation(instance)
        representation['products'] = [
            {
                'id': item.product.id,
                'name_uz': item.product.name_uz,
                'name_ru': item.product.name_ru,
                'name_en': item.product.name_en,
                'description_uz': item.product.description_uz,
                'description_ru': item.product.description_ru,
                'description_en': item.product.description_en,
                'amount': item.quantity,
                'price': item.product.price,
                'images': [
                    request.build_absolute_uri(image.image.url)
                    for image in item.product.images.all()
                ] if request else []
            } for item in instance.products.all()
        ]

        representation['user'] = {
            'id': instance.user.id,
            'name': instance.user.name,
            'phone_number': instance.user.phone_number
        } if instance.user else None

        return representation


class GeneratePaymentLinkSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)


class OrderHistoryIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['id', 'order', 'user', 'date', 'status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['order'] = OrderSerializer(instance.order).data
        return representation


class OrderHistoryBaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['id', 'order', 'user', 'date', 'status']

    def create(self, validated_data):
        order_history = super().create(validated_data)
        order = order_history.order
        order.status = order_history.status
        order.save()
        return order_history

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        order = instance.order
        order.status = instance.status
        order.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'stripe_charge_id', 'amount', 'created_at']


class DashboardSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    total_users = serializers.IntegerField()
    users_for_this_month = serializers.IntegerField()
    users_for_this_week = serializers.IntegerField()
    users_for_today = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_banner = serializers.IntegerField()
    orders_by_day = serializers.ListField(child=serializers.DictField())
    top_products = serializers.ListField(child=serializers.DictField())
    top_users = serializers.ListField(child=serializers.DictField())
    top_categories = serializers.ListField(child=serializers.DictField())


class DeliveryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = ['id', 'name_uz', 'name_ru', 'name_en']


class PolicyAndPrivacySerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyAndPrivacy
        fields = ['id', 'name_uz', 'name_ru', 'name_en']


class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ['id', 'name_uz', 'name_ru', 'name_en']


class ReturnPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnPolicy
        fields = ['id', 'name_uz', 'name_ru', 'name_en']
