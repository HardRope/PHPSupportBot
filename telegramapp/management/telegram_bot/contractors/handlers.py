from .state import ContractorState as State

from . import api, send


def check_access(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    # TODO вернуть проверку
    # is_active = api.is_active(chat_id)
    is_active = True

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
        # TODO мб не удалять сообщение от пользователя?
        # TODO save resume
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
        orders = [1, 2, 3]  # TODO implement and use get_available_orders(chat_id)
        send.available_orders(context, chat_id, message_id)
        return State.AVAILABLE_ORDERS.value

    if query.data == "current_orders":
        orders = [1, 2, 3]  # TODO implement and use get_current_orders(chat_id)
        send.orders(context, chat_id, message_id)
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


def available_order_detail_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data.startswith("take_"):
        order_id = query.data[
            5:
        ]  # TODO может быть лучше передать через redis или context
        send.time_estimate_request(context, chat_id, message_id, order_id)
        return State.TIME_ESTIMATE_REQUEST.value

    if query.data == "back":
        orders = [1, 2, 3]  # TODO implement and use get_available_orders(chat_id)
        send.available_orders(context, chat_id, message_id)
        return State.AVAILABLE_ORDERS.value


def process_time_estimate(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        # TODO get order from context or idk
        order_id = 5
        # TODO take order
        send.order_detail_private(
            context, chat_id, order_id, message_id, with_keyboard=False
        )
        send.home(context, chat_id)
        return State.HOME.value

    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        if query.data == "back":
            # TODO get order from context or idk
            order_id = 5  # Example of available order
            send.order_detail_public(context, chat_id, order_id)
            return State.AVAILABLE_ORDER_DETAIL.value


def orders_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data.isdigit():
        order_id = query.data
        send.order_detail_private(context, chat_id, order_id, message_id)
        return State.ORDER_DETAIL.value

    if query.data == "back":
        send.home(context, chat_id, message_id)
        return State.HOME.value


def order_detail_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data.startswith("complete_"):
        order_id = query.data[
            9:
        ]  # TODO может быть лучше передать через redis или context
        send.order_report_request(context, chat_id, order_id, message_id)
        return State.ORDER_REPORT_REQUEST.value

    if query.data == "back":
        orders = [1, 2, 3]  # TODO implement and use get_available_orders(chat_id)
        send.orders(context, chat_id, message_id)
        return State.ORDERS.value


def process_order_report(update, context):
    query = update.callback_query

    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        # TODO get order from context or idk
        order_id = 7  # Example taken order
        # TODO save report
        send.order_complete_confirmation(context, chat_id, order_id, message_id)
        return State.ORDER_COMPLETE_CONFIRMATION.value

    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        if query.data == "back":
            # TODO get order from context or idk
            order_id = 5
            send.order_detail_private(context, chat_id, order_id, message_id)
            return State.ORDER_DETAIL.value


def order_complete_confirmation_actions(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == "yes":
        # TODO actually complete order
        order_id = 7
        send.order_completed(context, chat_id, order_id, message_id)
        send.home(context, chat_id)
        return State.HOME.value

    if query.data == "no":
        order_id = 7
        send.order_detail_private(context, chat_id, order_id, message_id)
        return State.ORDER_DETAIL.value
