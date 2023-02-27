from django.contrib import admin

from orderapp.models import Person, Client, Manager, Contractor, Subscription, Order, Ticket, Messages
from paymentapp.models import Tariff


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['tg_username', 'tg_chat_id']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'active']


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'active']


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ['user', 'active']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['client', 'tariff', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'contractor', 'status', 'created_at']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'manager', 'status', 'created_at']


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['name', 'orders_amount', 'response_time', 'active']

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['client', 'contractor', 'order']