from textwrap import dedent

from .telegram_keyboards.manager_keyboards import (
    manager_main_menu,
    get_back_menu,
    active_tickets_menu,
    ticket_menu,
    active_orders_menu,
    free_contractors_menu
)
from .db_requests.manager_requests import (
    get_active_tickets,
    get_ticket,
    claim_ticket,
    get_active_orders,
    get_order,
    get_contractors,
    get_contractor,

)

def send_manager_main_menu(context, chat_id, message_id, message_text=None):
    default_text = 'Сервисное меню для менеджеров.'
    if message_text:
        message_text = f'{default_text} \n\n {message_text}'
    else:
        message_text = default_text

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=manager_main_menu()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_ticket_info(context, chat_id, message_id, ticket_collection):
    ticket_id = ticket_collection.get('ticket_id')
    description =  ticket_collection.get('description')
    order = ticket_collection.get('order', 'Не указан')
    client = ticket_collection.get('client', 'Не указан')
    if client != 'Не указан':
        client = '@' + client
    contractor = ticket_collection.get('contractor', 'Не указан')
    if contractor != 'Не указан':
        contractor = '@' + contractor
    created_at = ticket_collection.get('created_at')

    message_text = f'''Информация по заявке.
Дата заявки: {created_at}
Номер заявки: {ticket_id}
Текст заявки: {description}
Заказ {order}
Клиент: {client}
Исполнитель: {contractor}'''

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=ticket_menu(ticket_id)
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_active_orders(context, chat_id, message_id):
    message_text = 'Незавершённые заказы.'
    orders = get_active_orders()
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=active_orders_menu(orders)
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_order_info(context, chat_id, message_id, order_id):
    #TODO
    order_collection = get_order(order_id)

    description = order_collection.get('description')
    estimated_at = order_collection.get('estimated_at', 'Не указано')
    status = order_collection.get('status')
    client = order_collection.get('client_name', 'Не указан')
    if client != 'Не указан':
        client = '@' + client
    contractor = order_collection.get('contractor_name', 'Не указан')
    if contractor != 'Не указан':
        contractor = '@' + contractor

    message_text = f'''Заказ №{order_id}
Статус: {status}
Описание: {description}
Дата сдачи: {estimated_at}
Исполнитель: {contractor}
Заказчик: {client}
'''
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_back_menu()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_free_contractors(context, chat_id, message_id):
    contractors = get_contractors()
    message_text = 'Свободные исполнители.'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=free_contractors_menu(contractors)
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def manager_main_menu_handler(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        return

    if query.data == 'tickets':
        message_text = 'Необработанные заявки.'
        tickets = get_active_tickets()
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=active_tickets_menu(tickets=tickets)
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'ACTIVE_TICKETS'
    if query.data == 'orders':
        send_active_orders(context, chat_id, message_id)
        return 'ACTIVE_ORDERS'
    if query.data == 'contractors':
        send_free_contractors(context, chat_id, message_id)
        return 'FREE_CONTRACTORS'
    # if query.data == 'text':
    #     pass


def active_tickets_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
    else:
        ticket_id = query.data
        ticket_collection = get_ticket(ticket_id)
        send_ticket_info(context, chat_id, message_id, ticket_collection)
        return 'TICKET_HANDLER'


def ticket_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
    else:
        ticket_id = query.data
        if claim_ticket(chat_id, ticket_id):
            message_text = f'Вы взяли заявку {ticket_id}'
        else:
            message_text = 'Не получилось взять заявку.'
        send_manager_main_menu(context, chat_id, message_id, message_text)
        return 'MANAGER_MAIN_MENU'


def active_orders_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
    elif query.data.is_digit():
        order_id = query.data

        send_order_info(context, chat_id, message_id, order_id)
        return 'ORDER_HANDLER'


def order_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_active_orders(context, chat_id, message_id)
        return 'ACTIVE_ORDERS'


def free_contractors_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
    else:
        contractor_id = query.data
        contractor_username = get_contractor(contractor_id)
        message_text = f'Контакт исполнителя: @{contractor_username}'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_back_menu()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CONTRACTOR_HANDLER'

def contractor_contact_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_free_contractors(context, chat_id, message_id)
        return 'FREE_CONTRACTORS'
