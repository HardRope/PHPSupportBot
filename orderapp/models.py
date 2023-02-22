from django.contrib.auth.models import User
from django.db import models

from paymentapp.models import Tariff

class Person(User):
    tg_chat_id = models.CharField(
        max_length=64,
        null=True,
        verbose_name='ID чата Телеграм',
        unique=True,
    )
    tg_username = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        verbose_name='Имя пользователя в Телеграм',
    )


class Client(models.Model):
    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='clients',
        verbose_name='Учетная запись Телеграм',
    )
    active = models.BooleanField(verbose_name='Активен', db_index=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Manager(models.Model):
    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='managers',
        verbose_name='Учетная запись Телеграм',
    )
    active = models.BooleanField(verbose_name='Активен', db_index=True)

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'


class Сontractor(models.Model):
    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='contractors',
        verbose_name='Учетная запись Телеграм',
    )
    active = models.BooleanField(verbose_name='Активен', db_index=True)

    class Meta:
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'


class Subscription(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='subscribtions',
        verbose_name='Клиент',
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.SET_NULL,
        related_name='subscribtions',
        verbose_name='Тариф',
        null=True,
    )
    created_at = models.DateTimeField(verbose_name='Дата оформления')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новый'),
        ('WOR', 'В работе'),
        ('FIN', 'Завершен'),
        ('OVE', 'Просрочен')
    ]
    description = models.TextField(verbose_name='Описание', blank=True)
    contractor = models.ForeignKey(
        Сontractor,
        on_delete=models.SET_NULL,
        related_name='orders',
        verbose_name='Исполнитель',
        null=True,
        blank=True,
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Подписка',
    )
    created_at = models.DateTimeField(verbose_name='Создана', auto_now=True)
    estimated_at = models.DateTimeField(verbose_name='Истекает',
                                        null=True,
                                        blank=True)
    finished_at = models.DateTimeField(verbose_name='Закрыта',
                                       null=True,
                                       blank=True)
    status = models.CharField(max_length=3,
                              choices=STATUS_CHOICES,
                              verbose_name='Статус',
                              db_index=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новое'),
        ('WOR', 'В работе'),
        ('CLO', 'Закрыто'),
    ]
    description = models.TextField(verbose_name='Описание', blank=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name='tickets',
        verbose_name='По заявке',
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        Manager,
        on_delete=models.CASCADE,
        related_name='tickets',
        verbose_name='Ответственный менеджер',
    )
    created_at = models.DateTimeField(verbose_name='Создано', auto_now=True)
    closed_at = models.DateTimeField(verbose_name='Закрыто',
                                       null=True,
                                       blank=True)
    status = models.CharField(max_length=3,
                              choices=STATUS_CHOICES,
                              verbose_name='Статус',
                              db_index=True)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
