from textwrap import dedent

from .telegram_keyboards.manager_keyboards import (
    manager_main_menu,
    get_back_menu,
    tickets_menu,
    ticket_menu,
    active_orders_menu,
    free_contractors_menu,
)
from .db_requests.manager_requests import (
    get_active_tickets,
    get_ticket,
    claim_ticket,
    get_active_orders,
    get_order,
    get_contractors,
    get_contractor,
    get_manager_tickets,

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
    if context.user_data.get('claimed', None):
        reply_markup = get_back_menu()
    else:
        reply_markup = ticket_menu(ticket_id)

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=reply_markup
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


def send_manager_tickets(context, chat_id, message_id):
    message_text = 'Принятые заявки.'
    tickets = get_manager_tickets(chat_id)
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=tickets_menu(tickets=tickets)
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
            reply_markup=tickets_menu(tickets=tickets)
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        context.user_data['claimed'] = False
        return 'TICKETS'
    if query.data == 'orders':
        send_active_orders(context, chat_id, message_id)
        return 'ACTIVE_ORDERS'
    if query.data == 'contractors':
        send_free_contractors(context, chat_id, message_id)
        return 'FREE_CONTRACTORS'
    if query.data == 'manager_tickets':
        send_manager_tickets(context, chat_id, message_id)
        context.user_data['claimed'] = True
        return 'TICKETS'
    if str(query.data).isdigit():
        context.user_data['claimed'] = False
        ticket_id = query.data
        ticket_collection = get_ticket(ticket_id)
        send_ticket_info(context, chat_id, message_id, ticket_collection)
        return 'TICKET_HANDLER'


def tickets_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
    elif str(query.data).isdigit():
        ticket_id = query.data
        ticket_collection = get_ticket(ticket_id)
        send_ticket_info(context, chat_id, message_id, ticket_collection)
        return 'TICKET_HANDLER'
    else:
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'


def ticket_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        if context.user_data.get('claimed', None):
            send_manager_tickets(context, chat_id, message_id)
        else:
            message_text = 'Необработанные заявки.'
            tickets = get_active_tickets()
            context.bot.send_message(
                chat_id=chat_id,
                text=dedent(message_text),
                reply_markup=tickets_menu(tickets=tickets)
            )
            context.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
        return 'TICKETS'
    elif str(query.data).isdigit():
        ticket_id = query.data
        if claim_ticket(chat_id, ticket_id):
            message_text = f'Вы взяли заявку {ticket_id}'
        else:
            message_text = 'Не получилось взять заявку.'
        send_manager_main_menu(context, chat_id, message_id, message_text)
        return 'MANAGER_MAIN_MENU'
    else:
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'


def manager_orders_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
    elif str(query.data).isdigit():
        order_id = query.data

        send_order_info(context, chat_id, message_id, order_id)
        return 'ORDER_HANDLER'
    else:
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'


def order_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_active_orders(context, chat_id, message_id)
        return 'ACTIVE_ORDERS'
    else:
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'

def free_contractors_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
    elif str(query.data).isdigit():
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
    else:
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'


def contractor_contact_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_free_contractors(context, chat_id, message_id)
        return 'FREE_CONTRACTORS'
    else:
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'


def get_notification_handler(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        return

    if query.data and query.data == 'miss':
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
    else:
        send_manager_main_menu(context, chat_id, message_id)
        return 'MANAGER_MAIN_MENU'
