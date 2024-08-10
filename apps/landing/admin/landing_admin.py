from django.contrib import admin
from apps.landing.models.landing import *


admin.site.register(SpecialOffer)

admin.site.register(Company)

admin.site.register(SocialNetworks)

admin.site.register(News)


@admin.register(Recall)
class RecallAdmin(admin.ModelAdmin):
    list_display = ('client', 'name', 'phone', 'email', 'comment')
    search_fields = ('name', 'phone', 'email', 'client__username')