from django.contrib import admin
from apps.landing.models.landing import *

@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'product']
    search_fields = ['title_en', 'title_ru', 'title_uz']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    search_fields = ['title']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'company']
    search_fields = ['title_en', 'title_ru', 'title_uz']
    list_filter = ['company']


@admin.register(Recall)
class RecallAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'phone', 'email', 'comment')
    search_fields = ('name', 'phone', 'email', 'client__username')