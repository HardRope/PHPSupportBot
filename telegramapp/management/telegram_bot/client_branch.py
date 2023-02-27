import logging
from textwrap import dedent

from telegram import LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup

from .telegram_keyboards.client_keyboards import (
    get_client_main_menu,
    get_back_menu,
    get_orders_menu,
    get_order_menu,
    get_tariffs_menu,
    get_tariff_menu,
)
from .telegram_keyboards.manager_keyboards import new_ticket_menu
from .db_requests.client_requests import (
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
    buy_tariff,
    get_order_messages,
    create_order_message
)

from . import contractors


logger = logging.getLogger(__name__)

def send_client_main_menu(context, chat_id, message_id, message_text=None):
    subscription_details = get_subscription_details(chat_id)
    if subscription_details:
        context.user_data['tariff'] = subscription_details.get('tariff_name')
        context.user_data['orders_left'] = subscription_details.get('orders_left')
        default_text = f'''Ваш тариф: {subscription_details.get('tariff_name')}.
Осталось заявок по тарифу: {subscription_details.get('orders_left')}.
Дней до конца подписки: {subscription_details.get('time_left')}
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
    print('message_id', message_id)
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
    message_text = 'Доступные тарифы, выберите тариф для просмотра информации и покупки.'
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
        reply_markup=contractors.keyboards.incoming_message(order_id)
    )
    db.set(chat_id, contractors.State.INCOMING_MESSAGE.value)


def send_message_to_client(context, order_id, chat_id, contractor_text, db):
    message_text = f'Вам поступило сообщение от исполнителя (Заказ №{order_id}).' \
                   f'\nДля ответа позже перейдите в Заказ и введите сообщение.' \
                   f'\nСообщение:' \
                   f'\n{contractor_text}'

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=contractors.keyboards.incoming_message(order_id)  # TODO заменить на клавиатуру для заказчика
    )
    db.set(chat_id, 'NEW_MESSAGE_TO_CLIENT')


def send_message_to_manager(context, chat_id, ticket_id, ticket_text, db):
    message_text = f'Поступила новая заявка (Тикет №{ticket_id}) \n{ticket_text}'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=new_ticket_menu()
    )
    db.set(chat_id, 'NOTIFICATION')


def send_order_info(context, chat_id, message_id, order_id, order_collection, message_text=None):
    order_contractor = order_collection.get('contractor_name')
    if order_contractor:
        order_contractor = f'@{order_contractor}'
    else:
        order_contractor = 'Не выбран'
    default_text = f'''Информация по заказу №{order_id}
Текст заявки: {order_collection.get('description')}
Данные доступа: {order_collection.get('credentials')}
Статус: {order_collection.get('status')}
'''
    if context.user_data.get('tariff') == 'VIP':
        default_text += f'Исполнитель: {order_contractor}'
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
        return 'GET_TASK'

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


def get_task_handler(update, context):
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
        context.user_data['new_order'] = order_text

        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(f'Введите данные для доступа к сайту'),
            reply_markup=get_back_menu()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id - 1
        )
        return 'GET_CREDENTIALS'
    else:
        message_text = 'Невозможно создать заявку, пожалуйста, расширьте Ваш тариф.'
        send_client_main_menu(context, chat_id, message_id, message_text)
        return 'CLIENT_MAIN_MENU'


def get_credentials_handler(update, context):
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
        orders_left = context.user_data.get('orders_left')
        message_text = f'Для создания нового заказа просто отправьте сообщение с заданием. ' \
                       f'\nКоличество доступных заявок: {orders_left}'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_back_menu()
        )
        return 'GET_TASK'
    else:
        order_text = context.user_data.pop('new_order')
        credentials = update.message.text
        create_order(chat_id, order_text, credentials)

        message_text = 'Заявка успешно создана. Вы можете проверить её в списке активных заказов.'
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

    order_id = context.user_data.get('order_id')
    order_complete = context.user_data.get('order_complete')
    saved_state = context.user_data.get('state')
    contractor_id = context.user_data.get('contractor_id')

    if query and query.data == 'back':
        context.user_data.pop('order_id')
        context.user_data.pop('order_complete')
        context.user_data.pop('state')
        context.user_data.pop('contractor_id')
        if 'ACTIVE' in saved_state:
            send_active_orders(context, chat_id, message_id)
        else:
            send_complete_orders(context, chat_id, message_id)
        return saved_state
    if query and query.data == 'messages':
        messages = get_order_messages(chat_id, order_id)
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(f'История последних сообщений с исполнителем: \n {messages}'),
            reply_markup=get_back_menu()
        )
        return 'CLIENT_MESSAGES'
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

    if update.message.text:
        client_message = update.message.text

        if contractor_id:
            send_message_to_contractor(context, order_id, contractor_id, client_message, db)
            create_order_message(chat_id, contractor_id, order_id, client_message)
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
                message_id=message_id
            )
            send_active_orders(context, chat_id, message_id, message_text)

            return saved_state


def client_messages_handler(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
    else:
        return
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )
    return 'CLIENT_ORDER'


def tariffs_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_client_main_menu(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    elif query.data:
        tariff_name = query.data
        tariff = get_tariff(tariff_name)
        context.user_data['choosing_tariff'] = tariff

        title = f'Оплата подписки по тарифу {tariff.get("tariff_name")}'
        description = f'{tariff.get("description")}' \
                      f'\nКоличество заказов в тарифе: {tariff.get("orders_amount")} шт.' \
                      f'\nВремя ответа на заявку: {tariff.get("response_time")} ч.'
        payload = 'Custom-Payload'
        provider_token = context.bot_data['payment_token']
        currency = 'RUB'
        prices = [LabeledPrice("Стоимость", tariff.get("price") * 100)]

        context.bot.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            currency=currency,
            prices=prices,
            reply_markup=get_tariff_menu(),
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'PAYMENT'


def create_ticket_handler(update, context, db):
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
            send_message_to_manager(context, manager, ticket_id, ticket_text, db)

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
