from .state import ContractorState as State

from . import send, storage


def check_access(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    is_active = storage.is_active(chat_id)

    if not is_active:
        send.account_on_review(context, chat_id, message_id)
        return State.ACCOUNT_ON_REVIEW.value

    send.home(context, chat_id, message_id)
    return State.HOME.value


def process_resume(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        tg_username = update.message.chat.username
        resume = update.message.text
        # TODO мб не удалять сообщение от пользователя?
        storage.create_contractor(chat_id, tg_username, resume)
        send.account_on_review(context, chat_id, message_id, initial=True)
        return State.ACCOUNT_ON_REVIEW.value

    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        if query.data == "back":
            from telegramapp.management.telegram_bot.welcome_branch import (
                send_start_message,
            )

            send_start_message(context, chat_id, message_id)
            return "ROLE"


def home_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == "available_orders":
        orders = storage.get_available_orders(chat_id)
        send.available_orders(context, chat_id, message_id, orders)
        return State.AVAILABLE_ORDERS.value

    if query.data == "current_orders":
        orders = storage.get_orders(chat_id)
        send.orders(context, chat_id, message_id, orders)
        return State.ORDERS.value

    if query.data == "stats":
        send.stats(context, chat_id, message_id)
        return State.STATISTICS.value


def stats_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == "back":
        send.home(context, chat_id, message_id)
        return State.HOME.value


def available_orders_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data.isdigit():
        order_id = query.data
        send.order_detail_public(context, chat_id, order_id, message_id)
        return State.AVAILABLE_ORDER_DETAIL.value

    if query.data == "back":
        send.home(context, chat_id, message_id)
        return State.HOME.value


def available_order_detail_actions(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data.startswith("take_"):
        order_id = query.data[5:]
        db.set(f"{chat_id}_is_taking", order_id)

        send.time_estimate_request(context, chat_id, message_id, order_id)
        return State.TIME_ESTIMATE_REQUEST.value

    if query.data == "back":
        orders = storage.get_available_orders(chat_id)
        send.available_orders(context, chat_id, message_id, orders)
        return State.AVAILABLE_ORDERS.value


def process_time_estimate(update, context, db):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

        order_id = db.get(f"{chat_id}_is_taking")

        time_estimate_days = int(update.message.text)

        send.order_detail_full(
            context, chat_id, order_id, message_id, with_keyboard=False
        )
        storage.take_order(order_id, chat_id, time_estimate_days)
        db.getdel(f"{chat_id}_is_taking")
        
        send.home(context, chat_id)
        return State.HOME.value

    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        if query.data == "back":
            order_id = db.get(f"{chat_id}_is_taking")
            send.order_detail_public(context, chat_id, order_id)
            return State.AVAILABLE_ORDER_DETAIL.value


def orders_actions(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data.isdigit():
        order_id = query.data
        send.order_detail_full(context, chat_id, order_id, message_id)
        db.set(f"{chat_id}_is_viewing", order_id)
        return State.ORDER_DETAIL.value

    if query.data == "back":
        send.home(context, chat_id, message_id)
        return State.HOME.value


def order_detail_actions(update, context, db):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        order_id = db.get(f"{chat_id}_is_viewing")
        client_chat_id = storage.get_client_chat_id_by_order(order_id)
        text = update.message.text
        from telegramapp.management.telegram_bot.client_branch import send_message_to_client
        send_message_to_client(context, order_id, client_chat_id, text, db)
        send.order_detail_full(context, chat_id, order_id, message_id)
        return State.ORDER_DETAIL.value


    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        if query.data.startswith("complete_"):
            order_id = int(query.data[9:])
            send.order_report_request(context, chat_id, order_id, message_id)
            return State.ORDER_REPORT_REQUEST.value

        if query.data == "back":
            orders = storage.get_orders(chat_id)
            db.getdel(f"{chat_id}_is_viewing")
            send.orders(context, chat_id, message_id, orders)
            return State.ORDERS.value


def process_order_report(update, context, db):
    query = update.callback_query

    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        order_id = db.get(f"{chat_id}_is_viewing")
        db.set(f"{chat_id}_is_writing_report", update.message.text)
        send.order_complete_confirmation(context, chat_id, order_id, message_id)
        return State.ORDER_COMPLETE_CONFIRMATION.value

    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        if query.data == "back":
            order_id = db.get(f"{chat_id}_is_viewing")
            send.order_detail_full(context, chat_id, order_id, message_id)
            return State.ORDER_DETAIL.value


def order_complete_confirmation_actions(update, context, db):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == "yes":
        order_id = db.get(f"{chat_id}_is_viewing")
        
        report_text = db.get(f"{chat_id}_is_writing_report")
        storage.close_order(order_id, report_text)
        db.getdel(f"{chat_id}_is_writing_report")

        send.order_completed(context, chat_id, order_id, message_id)
        send.home(context, chat_id)
        return State.HOME.value

    if query.data == "no":
        order_id = 7
        send.order_detail_full(context, chat_id, order_id, message_id)
        db.getdel(f"{chat_id}_is_writing_report")
        return State.ORDER_DETAIL.value


def incoming_message_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == "read":
        send.home(context, chat_id)
        return State.HOME.value

    if query.data.isdigit():
        order_id = query.data
        # TODO: set current order in redis or context?
        send.order_detail_full(context, chat_id, order_id, message_id)
        return State.ORDER_DETAIL.value
