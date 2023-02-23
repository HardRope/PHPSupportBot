import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from orderapp.models import Person, Contractor, Client, Manager, Order, Ticket
from paymentapp.models import Tariff


#TODO: проверка статуса контрактора (авторизован/неавторизован) -> True, False
def is_contractor_authorized(tg_chat_id):
    try:
        contractor = Contractor.objects.get(user__tg_chat_id=tg_chat_id)
        if not contractor.active:
            return False
        return True
    except ObjectDoesNotExist:
        return False

#TODO: проверка роли пользователя (менеджер, контрактор, клиент) -> str
def check_user_role(tg_chat_id):
    try:
        user = Person.objects.get(tg_chat_id=tg_chat_id)
        if hasattr(user, 'client'):
            return 'client'
        elif hasattr(user, 'manager'):
            return 'manager'
        elif hasattr(user, 'contractor'):
            return 'contractor'
        else:
            return None
    except ObjectDoesNotExist:
        return None
    

def get_or_create_user(tg_chat_id, tg_username, username=None):
    username = tg_username if not username else username
    user, created = Person.objects.get_or_create(tg_chat_id=tg_chat_id,
                                                 tg_username=tg_username,
                                                 username=username,
                                                 password=tg_chat_id)
    return user


#TODO: создание контрактора -> None
def create_contractor(tg_chat_id, tg_username, resume, username=None):
    user = get_or_create_user(tg_chat_id, tg_username, username)
    contractor, created = Contractor.objects.get_or_create(user=user, resume=resume)
    return

#TODO: создание клиента -> None
def create_client(tg_chat_id, tg_username, username=None):
    user = get_or_create_user(tg_chat_id, tg_username, username)
    client, created = Client.objects.get_or_create(user=user)
    return

#TODO: список активных заказов клиента -> [id's]
def get_active_orders(tg_chat_id):
    client = Client.objects.get(user__tg_chat_id=tg_chat_id)
    active_orders = Order.objects.filter(subscription__client=client)\
                                 .exclude(status='FIN')
    return list(active_orders)

#TODO: список выполненных заказов клиента -> [id's]
def get_active_orders(tg_chat_id):
    client = Client.objects.get(user__tg_chat_id=tg_chat_id)
    finished_orders = Order.objects.filter(subscription__client=client)\
                                 .filter(status='FIN')
    return list(finished_orders)

#TODO: получение заказа по id -> json
def get_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        return serializers.serialize('json', list(order))
    except ObjectDoesNotExist:
        return None

#TODO: создание тикета -> None
def create_ticket(description, client_chat_id=None, order_id=None):
    if client_chat_id:
        client = Client.objects.get(user__tg_chat_id=client_chat_id)
    if order_id:
        order = Order.objects.get(id=order_id)
    ticket = Ticket.objects.create(
        description=description,
        client=client,
        order=order,
    )
    return ticket.id

#TODO: список тарифов -> [name's]
def get_tariff_names():
    return [tariff.name for tariff in Tariff.objects.all()]

#TODO: инфо о тарифе -> json
def get_tariff(tariff_name):
    try:
        tariff = Order.objects.get(name=tariff_name)
        return serializers.serialize('json', list(tariff))
    except ObjectDoesNotExist:
        return None

#TODO: 

#TODO:

#TODO:

#TODO:

#TODO:

#TODO:

#TODO: