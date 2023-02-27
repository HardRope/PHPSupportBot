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

    def __str__(self):
        return self.tg_chat_id

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Client(models.Model):
    user = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    active = models.BooleanField(verbose_name='Активен', default=False, db_index=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Manager(models.Model):
    user = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    active = models.BooleanField(verbose_name='Активен', default=False, db_index=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'


class Contractor(models.Model):
    user = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    active = models.BooleanField(verbose_name='Активен', default=False, db_index=True)
    resume = models.TextField(verbose_name='Резюме', blank=True)

    def __str__(self):
        return self.user.username

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
    created_at = models.DateTimeField(
        verbose_name='Дата оформления',
        auto_now_add=True,
    )

    def __str__(self):
        return self.tariff.name

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
    credentials = models.TextField(verbose_name='Данные для админки', blank=True)
    contractor = models.ForeignKey(
        Contractor,
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
                              default='NEW',
                              db_index=True)
    
    def __str__(self):
        return str(self.pk)

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
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        related_name='tickets',
        verbose_name='Подано клиентом',
        null=True,
        blank=True,
    )
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
        on_delete=models.SET_NULL,
        related_name='tickets',
        verbose_name='Ответственный менеджер',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(verbose_name='Создано', auto_now=True)
    closed_at = models.DateTimeField(verbose_name='Закрыто',
                                       null=True,
                                       blank=True)
    status = models.CharField(max_length=3,
                              choices=STATUS_CHOICES,
                              verbose_name='Статус',
                              default='NEW',
                              db_index=True)
    
    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'


class Messages(models.Model):
    contractor = models.ForeignKey(
        Contractor,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Исполнитель',
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Заказчик',
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='К заказу',
    )

    text = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
