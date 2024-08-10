from django.contrib import admin
from apps.landing.models.landing import *

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'product']
    search_fields = ['title_en', 'title_ru', 'title_uz']

admin.site.register(Company)

@admin.register(SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'link')
    search_fields = ('company__name', 'name', 'link')
    list_filter = ('company',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'company']
    search_fields = ['title_en', 'title_ru', 'title_uz']
    list_filter = ['company']


@admin.register(Recall)
class RecallAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'phone', 'email', 'comment')
    search_fields = ('name', 'phone', 'email', 'client__username')