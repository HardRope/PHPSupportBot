from django.db import models

from orderapp.models import Order

class OrderSummary(Order):
    class Meta:
        proxy = True
        verbose_name = 'Статистика по заявке'
        verbose_name_plural = 'Статистика по заявкам'