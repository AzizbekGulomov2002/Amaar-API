from django.contrib import admin

from apps.orders.models.infos import DeliveryInfo, PolicyAndPrivacy, PublicOffer, ReturnPolicy, Banner


admin.site.register(Banner)


@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')


@admin.register(PolicyAndPrivacy)
class PolicyAndPrivacyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')


@admin.register(PublicOffer)
class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')


@admin.register(ReturnPolicy)
class ReturnPolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'name_ru', 'name_en')
