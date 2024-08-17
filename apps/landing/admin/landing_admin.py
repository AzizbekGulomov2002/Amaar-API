from django.contrib import admin

from apps.landing.models.landing import *


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    ...


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    ...


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    ...


@admin.register(SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    ...


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    ...


@admin.register(Recall)
class RecallAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'phone', 'email', 'comment')
    search_fields = ('name', 'phone', 'email', 'client__username')
