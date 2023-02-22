from django.db import models


class Tariff(models.Model):
    name = models.CharField(
        max_length=16,
        verbose_name='Название',
        blank=True,
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    price = models.IntegerField(verbose_name='Цена')
    orders_amount = models.IntegerField(verbose_name='Количество заявок')
    response_time = models.IntegerField(verbose_name='Время ответа (в часах)')
    order_cost = models.IntegerField(verbose_name='Стоимость выполнения одной заявки')
    active = models.BooleanField(verbose_name='Активен', db_index=True)

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
