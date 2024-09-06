from rest_framework import serializers

from apps.orders.models.infos import Banner, DeliveryInfo, PolicyAndPrivacy, PublicOffer, ReturnPolicy


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


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
