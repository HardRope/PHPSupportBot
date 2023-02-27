from datetime import date, datetime, time, timedelta

from django.core.exceptions import ObjectDoesNotExist

from orderapp.models import Contractor, Order
from telegramapp.management.telegram_bot.db_requests.welcome_db_requests import (
    get_or_create_user,
)

def is_active(tg_chat_id):
    try:
        contractor = Contractor.objects.get(user__tg_chat_id=tg_chat_id)
        if not contractor.active:
            return False
        return True
    except ObjectDoesNotExist:
        return False


def create_contractor(chat_id, tg_username, resume, username=None):
    user = get_or_create_user(chat_id, tg_username, username)
    contractor, created = Contractor.objects.get_or_create(user=user, resume=resume)


def get_available_orders(chat_id):
    # optionally filter by tg_chat_id (For example if the client has prefernces)
    orders = Order.objects.filter(status="NEW", contractor__isnull=True, subscription__isnull=False).only("id")
    return orders

def get_orders(chat_id):
    contractor = Contractor.objects.get(user__tg_chat_id=chat_id)
    orders = Order.objects.filter(status__in=["WOR", "OVE"], contractor=contractor, subscription__isnull=False).only("id")
    return orders


def get_order_public_detail(order_id):
    public_detail = Order.objects.get(id=order_id).description
    return public_detail

def get_order_full_detail(order_id):
    public_detail = Order.objects.get(id=order_id).description
    pricate_detail = Order.objects.get(id=order_id).description
    return f"{public_detail}\n\nДанные для админки:\n{pricate_detail}"


def take_order(order_id, chat_id, time_estimate_days):
    order = Order.objects.get(id=order_id)
    contractor = Contractor.objects.get(user__tg_chat_id=chat_id)

    estimated_at = datetime.combine(date.today() + timedelta(days=time_estimate_days), time.max)
    order.estimated_at = estimated_at
    order.contractor = contractor
    order.status = "WOR"
    order.save()


def get_client_chat_id_by_order(order_id):
    order = Order.objects.get(id=order_id)
    client = order.subscription.client
    return client.user.tg_chat_id

def close_order(order_id, text):
    order = Order.objects.get(id=order_id)

    order.status = "FIN"
    order.finished_at = datetime.now()
    order.description = order.description + f"\n\nОтчет:\n{text}"
    order.save()
