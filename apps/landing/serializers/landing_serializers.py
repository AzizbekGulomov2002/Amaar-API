from rest_framework import serializers

from apps.landing.models.landing import *


class SpecialOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = ['id', 'image', 'title_uz', 'title_ru', 'title_en', 'product']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = {
            'id': instance.product.id,
            'name_uz': instance.product.name_uz,
            'name_ru': instance.product.name_ru,
            'name_en': instance.product.name_en,
            'price': instance.product.price,
            'amount': instance.product.amount,
        }
        return representation


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class SocialNetworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetworks
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["id", 'title_uz', 'title_ru', 'title_en', 'desc_uz', 'desc_ru', 'desc_en', 'image', 'company']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['company'] = {
            'title': instance.company.title,
            'url': instance.company.url
        }
        return representation


class RecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recall
        fields = ["id", 'client', 'phone', 'name', 'email', 'comment']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['client'] = {
            'phone_number': instance.client.phone_number,
            'name': instance.client.name
        }
        return representation
