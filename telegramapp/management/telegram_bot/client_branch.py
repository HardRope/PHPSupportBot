import json
from textwrap import dedent

from .telegram_keyboards.client_keyboards import (
    get_client_main_menu,
    get_back_menu,
    get_active_orders_menu,
    get_complete_orders_menu,
    get_order_menu,
    get_tariffs_menu,
    get_tariff_menu,
)


def send_main_menu_message(context, chat_id, message_id, message_text=None):
    default_text = 'Ваш тариф такой-то, заявок осталось столько-то, ещё какая-то важная инфа.'
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
    default_text = 'Сейчас в работе N заказов'
    if message_text:
        message_text = f'{default_text} \n\n {message_text}'
    else:
        message_text = default_text

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_active_orders_menu()
    )

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_complete_orders(context, chat_id, message_id, message_text=None):
    default_text = 'Список завершённых заказов'
    if message_text:
        message_text = f'{default_text} \n\n {message_text}'
    else:
        message_text = default_text
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_complete_orders_menu(),
    )

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def send_tariffs(context, chat_id, message_id):
    message_text = 'Доступные тарифы, Ваш тариф, инфо о тарифах, для покупки - выберите тариф.'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_tariffs_menu()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def client_main_menu_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'create':
        message_text = 'Для создания нового заказа просто отправьте сообщение с заданием.'
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
        send_main_menu_message(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    else:
        # TODO: создать order
        order_text = update.message.text

        message_text = 'Заявка успешно создана. Вы можете проверить её в списке активных заказов'
        send_main_menu_message(context, chat_id, message_id, message_text)
        return 'CLIENT_MAIN_MENU'


def active_orders_handler(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_main_menu_message(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    if query.data.isdigit():

        user = f"user_tg_{chat_id}"
        db.set(
            user,
            json.dumps({
                'order_id': query.data,
                'state': 'CLIENT_ACTIVE_ORDERS'
            })
        )

        message_text = 'Инфо о заказе.   Для отправки сообщения исполнителю, введите его в чат'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_order_menu()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CLIENT_ORDER'


def complete_orders_handler(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if query.data == 'back':
        send_main_menu_message(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    if query.data.isdigit():
        user = f"user_tg_{chat_id}"
        db.set(
            user,
            json.dumps({
                'order_id': query.data,
                'state': 'CLIENT_COMPLETE_ORDERS'
            })
        )

        message_text = 'Инфо о заказе.'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_order_menu()
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CLIENT_ORDER'


def get_order_handler(update, context, db):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

    user = f"user_tg_{chat_id}"
    order_id = json.loads(db.get(user))['order_id']
    saved_state = json.loads(db.get(user))['state']

    if query and query.data == 'back':
        db.getdel(user)
        if 'ACTIVE' in saved_state:
            send_active_orders(context, chat_id, message_id)
        else:
            send_complete_orders(context, chat_id, message_id)
        return saved_state

    # TODO: проверка, выполнен ли заказ
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

    # TODO: проверить, выполнен ли заказ, переслать вопрос исполнителю
    send_client_answer = update.message.text
    message_text = 'Ваш вопрос исполнителю отправлен'

    if 'ACTIVE' in saved_state:
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(f'Сообщение по заказу {order_id}: \n {send_client_answer}'),
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id - 1
        )
        db.getdel(user)
        send_active_orders(context, chat_id, message_id, message_text)

        return saved_state


def tariffs_handler(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_main_menu_message(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    elif query.data:
        user = f"user_tg_{chat_id}"
        db.set(user, json.dumps({'tariff_name': query.data,}))
        message_text = 'Инфо о тарифе, стоимость тарифа, для покупки нажмите "Купить"'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
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
        # TODO: прикручиваем оплату
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

    try:
        user = f"user_tg_{chat_id}"
        saved_state = json.loads(db.get(user))['state']
        db.getdel(user)
    except:
        saved_state = None

    if query and query.data == 'back':
        send_main_menu_message(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    else:
        # TODO: создать ticket
        ticket_text = update.message.text
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

        send_main_menu_message(context, chat_id, message_id, message_text)
        return 'CLIENT_MAIN_MENU'
