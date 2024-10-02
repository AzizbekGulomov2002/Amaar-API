from django.db import models


class TelegramChannel(models.Model):
    name = models.CharField(max_length=255)
    group_id = models.CharField(max_length=255)
    basic = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' ' + self.group_id
    
    class Meta:
        verbose_name = "Telegram channel"
        verbose_name_plural = "Telegram channels"
