import json
from textwrap import dedent

from .telegram_keyboards.client_keyboards import (
    get_client_main_menu,
    get_back_menu,
    get_orders_menu,
    get_order_menu,
    get_tariffs_menu,
    get_tariff_menu,
)
from .telegram_keyboards.contractor_keyboards import new_message_menu
from .telegram_keyboards.manager_keyboards import new_ticket_menu
from .db_requests.db_requests import (
    get_active_orders,
    get_complete_orders,
    get_order,
    get_tariff_names,
    get_tariff,
    get_subscription_details,
    create_order,
    add_text_to_order,
    create_ticket,
    get_active_managers,
)


def send_client_main_menu(context, chat_id, message_id, message_text=None):
    subscription_details = get_subscription_details(chat_id)
    if subscription_details:
        context.user_data['tariff'] = subscription_details.get('tariff_name')
        context.user_data['orders_left'] = subscription_details.get('orders_left')
        default_text = f'''Ваш тариф: {subscription_details.get('tariff_name')}.
Осталось заявок по тарифу: {subscription_details.get('orders_left')}.
Другая справочная информация.'''
    else:
        context.user_data['tariff'] = None
        context.user_data['orders_left'] = 0
        default_text = 'В данный момент у Вас нет оплаченного тарифа.' \
                       '\nДля подключения перейдите в меню "Тарифы" и оплатите подходящий Вам тариф.' \
                       '\nДругая справочная информация.'

    if message_text:
        message_text = f'{default_text} \n\n {message_text}'
    else:
        message_text = default_text

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_client_main_menu()
    )

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_active_orders(context, chat_id, message_id, message_text=None):
    active_orders = get_active_orders(chat_id)
    orders_count = len(active_orders)

    default_text = f'Количество заказов в работе: {orders_count}'
    if message_text:
        message_text = f'{default_text} \n\n {message_text}'
    else:
        message_text = default_text

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_orders_menu(active_orders)
    )

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_complete_orders(context, chat_id, message_id, message_text=None):
    complete_orders = get_complete_orders(chat_id)
    order_count = len(complete_orders)

    default_text = f'Список завершённых заказов. Всего заказов завершено: {order_count}'
    if message_text:
        message_text = f'{default_text} \n\n {message_text}'
    else:
        message_text = default_text
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_orders_menu(complete_orders),
    )

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_tariffs(context, chat_id, message_id):
    tariffs = get_tariff_names()
    message_text = 'Доступные тарифы, Ваш тариф, инфо о тарифах, для покупки - выберите тариф.'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_tariffs_menu(tariffs)
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_message_to_contractor(context, order_id, chat_id, client_text, db):
    message_text = f'Вам поступило сообщение от заказчика (Заказ №{order_id}).' \
                   f'\nДля ответа позже перейдите в Заказ и введите сообщение.' \
                   f'\nСообщение:' \
                   f'\n{client_text}'

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=new_message_menu(order_id)
    )
    db.set(chat_id, 'GET_MESSAGE')


def send_message_to_manager(context, chat_id, ticket_id):
    message_text = f'Новая заявка от клиента'

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=new_ticket_menu(ticket_id)
    )


def send_order_info(context, chat_id, message_id, order_id, order_collection, message_text=None):
    order_contractor = order_collection.get('contractor_name')
    default_text = f'''Информация по заказу №{order_id}
Текст заявки: {order_collection.get('description')}
Статус: {order_collection.get('status')}
'''
    if context.user_data.get('tariff') == 'VIP':
        default_text += f'Исполнитель: @{order_contractor}'
    else:
        default_text += '\nДля того, чтобы увидеть контакт исполнителя, расширьте Ваш тариф до VIP'

    if message_text:
        message_text = f'{default_text} \n\n {message_text}'
    else:
        message_text = default_text

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_order_menu()
    )


def client_main_menu_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'create':
        orders_left = context.user_data.get('orders_left')
        message_text = f'Для создания нового заказа просто отправьте сообщение с заданием. ' \
                       f'\nКоличество доступных заявок: {orders_left}'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_back_menu()
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CREATE_ORDER'

    if query.data == 'active':
        send_active_orders(context, chat_id, message_id)
        return 'CLIENT_ACTIVE_ORDERS'

    if query.data == 'complete':
        send_complete_orders(context, chat_id, message_id)
        return 'CLIENT_COMPLETE_ORDERS'

    if query.data == 'tariffs':
        send_tariffs(context, chat_id, message_id)
        return 'TARIFFS'

    if query.data == 'ticket':
        message_text = 'Чтобы задать вопрос менеджеру, отправьте сообщение и мы свяжемся с Вами в ближайшее время.'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_back_menu()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CREATE_TICKET'


def create_order_handler(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        return

    if query and query.data == 'back':
        send_client_main_menu(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'

    if context.user_data.get('orders_left'):
        order_text = update.message.text
        create_order(chat_id, order_text)

        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(f'Ваша заявка: \n {order_text}'),
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id - 1
        )

        message_text = 'Заявка успешно создана. Вы можете проверить её в списке активных заказов'
    else:
        message_text = 'Невозможно создать заявку, пожалуйста, расширьте Ваш тариф.'
    send_client_main_menu(context, chat_id, message_id, message_text)
    return 'CLIENT_MAIN_MENU'


def active_orders_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_client_main_menu(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    if query.data.isdigit():
        order_id = query.data
        order_collection = get_order(order_id)

        context.user_data['order_id'] = order_id
        context.user_data['order_complete'] = False
        context.user_data['state'] = 'CLIENT_ACTIVE_ORDERS'
        context.user_data['contractor_id'] = order_collection.get('contractor_chat_id')

        message_text = '\n\n Для отправки сообщения исполнителю, просто введите его в чат.' \
                       '\nЕсли исполнитель ещё не выбран, мы добавим Ваше сообщение к тексту заявки'
        send_order_info(context, chat_id, message_id, order_id, order_collection, message_text)
        return 'CLIENT_ORDER'


def complete_orders_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_client_main_menu(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    if query.data.isdigit():
        order_id = query.data
        order_collection = get_order(order_id)

        context.user_data['order_id'] = order_id
        context.user_data['order_complete'] = True
        context.user_data['state'] = 'CLIENT_COMPLETE_ORDERS'

        send_order_info(context, chat_id, message_id, order_id, order_collection)
        return 'CLIENT_ORDER'


def get_order_handler(update, context, db):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        return

    order_id = context.user_data.pop('order_id')
    order_complete = context.user_data.pop('order_complete')
    saved_state = context.user_data.pop('state')
    contractor_id = context.user_data.pop('contractor_id')

    if query and query.data == 'back':
        if 'ACTIVE' in saved_state:
            send_active_orders(context, chat_id, message_id)
        else:
            send_complete_orders(context, chat_id, message_id)
        return saved_state

    if query and query.data == 'ticket':
        message_text = 'Чтобы задать вопрос менеджеру, отправьте сообщение и мы свяжемся с Вами в ближайшее время.'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_back_menu()
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CREATE_TICKET'


    client_message = update.message.text

    if contractor_id:
        send_message_to_contractor(context, order_id, contractor_id, client_message, db)
    else:
        add_text_to_order(order_id, client_message)

    if not order_complete:
        message_text = 'Ваш вопрос исполнителю отправлен'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(f'Сообщение по заказу {order_id}: \n {client_message}'),
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id - 1
        )
        send_active_orders(context, chat_id, message_id, message_text)

        return saved_state


def tariffs_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_client_main_menu(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    elif query.data:
        context.user_data['choosing_tariff'] = query.data
        tariff = get_tariff(query.data)

        message_text = 'Инфо о тарифе, стоимость тарифа, для покупки нажмите "Купить"'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(f'{tariff}'),
            reply_markup=get_tariff_menu()
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'TARIFF'


def tariff_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_tariffs(context, chat_id, message_id)
        return 'TARIFFS'
    elif query.data:
        tariff = context.user_data['choosing_tariff']
        # TODO: прикручиваем оплату
        return 'PAYMENT'


def create_ticket_handler(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        return

    if query and query.data == 'back':
        send_client_main_menu(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    else:
        ticket_text = update.message.text
        order_id = context.user_data.pop('order_id', None)
        saved_state = context.user_data.pop('state', None)

        ticket_id = create_ticket(ticket_text, chat_id, order_id)
        managers = get_active_managers()
        for manager in managers:
            send_message_to_manager(context, manager, ticket_id)

        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(f'Ваш вопрос менеджеру: \n {ticket_text}'),
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id - 1
        )

        message_text = 'Сообщение менеджеру отправлено'
        if saved_state:
            if 'ACTIVE' in saved_state:
                send_active_orders(context, chat_id, message_id, message_text)
            else:
                send_complete_orders(context, chat_id, message_id, message_text)
            return saved_state

        send_client_main_menu(context, chat_id, message_id, message_text)
        return 'CLIENT_MAIN_MENU'
