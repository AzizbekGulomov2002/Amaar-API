from django.contrib import admin

from apps.orders.models.telegram_chennels import TelegramChannel


@admin.register(TelegramChannel)
class TelegramChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_id', 'basic')
    list_filter = ('basic',)
    search_fields = ('name', 'group_id')
