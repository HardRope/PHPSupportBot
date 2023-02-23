import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from orderapp.models import Person, Contractor, Client, Manager, Order, Ticket, Subscription
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
    active_orders_id = [order.id for order in active_orders]
    return active_orders_id

#TODO: список выполненных заказов клиента -> [id's]
def get_complete_orders(tg_chat_id):
    client = Client.objects.get(user__tg_chat_id=tg_chat_id)
    finished_orders = Order.objects.filter(subscription__client=client)\
                                 .filter(status='FIN')
    finished_orders_id = [order.id for order in finished_orders]
    return finished_orders_id

#TODO: получение заказа по id -> json  + подгрузить tg_id и tg_username исполнителя
def get_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        contractor_name = order.contractor.user.username if order.contractor else None
        contractor_chat_id = order.contractor.user.tg_chat_id if order.contractor else None
        return {
            'description': order.description,
            'estimated_at': order.estimated_at,
            'status': order.get_status_display(),
            'contractor_name': contractor_name,
            'contractor_chat_id': contractor_chat_id,
        }
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
        tariff = Tariff.objects.get(name=tariff_name)
        return {
            'tariff_name': tariff.name,
            'description': tariff.description,
            'price': tariff.price,
            'orders_amount': tariff.orders_amount,
            'response_time': tariff.response_time,
            'order_cost': tariff.order_cost,
            'active': tariff.active,
        }
    except ObjectDoesNotExist:
        return None

#TODO: создание заказа -> result(True, False)
def create_order(tg_chat_id, description):
    try:
        subscription = Subscription.objects.get(client__user__tg_chat_id=tg_chat_id)
        order = Order.objects.create(
            description=description,
            subscription=subscription,
        )
        if not order:
            return False
        return True
    except ObjectDoesNotExist:
        return False

#TODO: данные о подписке юзера -> None, tariff.name
def get_subscription_details(tg_chat_id):
    try:
        subscription = Subscription.objects.get(client__user__tg_chat_id=tg_chat_id)
        orders_left = subscription.tariff.orders_amount - subscription.orders.count()
        return {
            'tariff_name': subscription.tariff.name,
            'orders_left': orders_left,
        }
    except ObjectDoesNotExist:
        return False

#TODO: список tg_id активных менеджеров -> [tg_id's]
def get_active_managers():
    return [manager.user.tg_chat_id for manager in Manager.objects.filter(active=True)]

#TODO:

#TODO:

#TODO:

#TODO: