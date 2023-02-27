from django.core.exceptions import ObjectDoesNotExist
from orderapp.models import Person, Contractor, Client, Manager, Order, Ticket, Subscription
from paymentapp.models import Tariff

def get_active_tickets():
    # TODO: вернуть список id необработанных заявок (без менеджера) -> [id's]
    tickets = Ticket.objects.filter(manager=None)
    tickets_id = [ticket.id for ticket in tickets]
    return tickets_id


def get_ticket(ticket_id):
    # TODO: вернуть всю инфу по тикету  -> dict
    ticket = Ticket.objects.get(id=ticket_id)
    ticket_order = ticket.order.id if ticket.order else 'Не указан'
    client_username = ticket.client.user.username if ticket.client else 'Не указан'

    contractor_username = ticket.order.contractor.user.username if ticket.order and ticket.order.contractor else 'Не указан'

    ticket_collection = {
        'ticket_id': ticket_id,
        'description': ticket.description,
        'order': ticket_order,
        'client': client_username,
        'contractor': contractor_username,
        'created_at': ticket.created_at.strftime("%d/%m/%Y, %H:%M:%S")
    }
    return ticket_collection


def claim_ticket(tg_chat_id, ticket_id):
    #TODO: закрепить заявку за менеджером -> True, False
    ticket = Ticket.objects.get(id=ticket_id)
    manager = Manager.objects.get(user__tg_chat_id=tg_chat_id)
    if not ticket.manager:
        ticket.manager = manager
        ticket.save()
        return True
    else:
        return False


def get_active_orders():
    #TODO: список незавершённых заказов -> [id's]
    orders = Order.objects.exclude(status='FIN')
    orders_id = [order.id for order in orders]
    return orders_id


def get_order(order_id):
    #TODO: вся инфа по ордеру -> dict
    try:
        order = Order.objects.get(id=order_id)
        contractor_name = order.contractor.user.username if order.contractor else None
        client_name = order.client.username
        return {
            'description': order.description,
            'estimated_at': order.estimated_at.strftime("%d/%m/%Y, %H:%M:%S"),
            'status': order.get_status_display(),
            'client_name': client_name,
            'contractor_name': contractor_name,
        }
    except ObjectDoesNotExist:
        return None


def get_contractors():
    #TODO: список айдишников незанятых исполнителей -> [{tg_id: username}]
    contractors = Contractor.objects.filter(active=True).filter(orders=None)
    contractor_collections = [{'tg_id': contractor.user.tg_chat_id, 'username': contractor.user.username} for contractor in contractors]
    return contractor_collections


def get_contractor(tg_chat_id):
    #TODO: контакт исполнителя -> username
    contractor = Contractor.objects.get(user__tg_chat_id=tg_chat_id)
    return contractor.user.username


def get_manager_tickets(tg_chat_id):
    #TODO: тикеты менеджера -> [id's]
    manager = Manager.objects.get(user__tg_chat_id=tg_chat_id)
    tickets = Ticket.objects.filter(manager=manager)
    tickets_id = [ticket.id for ticket in tickets]
    return tickets_id
