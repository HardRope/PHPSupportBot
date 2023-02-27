from textwrap import dedent

from . import storage
from . import keyboards as kbs


CONTRACTOR_TOS = """
Terms of Service:
1. Нормально делай
2. Нормально будет
"""


def tos(context, chat_id, prev_message_id=None):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    context.bot.send_message(chat_id=chat_id, text=dedent(CONTRACTOR_TOS))


RESUME_REQUEST_TEXT = "Отправьте нам небольшое текстовое описание себя"


def resume_request(context, chat_id, prev_message_id=None):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    context.bot.send_message(
        chat_id=chat_id, text=RESUME_REQUEST_TEXT, reply_markup=kbs.BACK
    )


def _home_text():
    return f"N активных заказов"


def home(context, chat_id, prev_message_id=None):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    context.bot.send_message(
        chat_id=chat_id, text=dedent(_home_text()), reply_markup=kbs.home()
    )


def account_on_review(context, chat_id, prev_message_id, initial=False):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    text = "Заявка ещё находится на рассмотрении."
    if initial:
        text = "Ваша заявка принята, зайдите позже, чтобы проверить статус заявки."  # TODO мб написать "мы вам напишем, когда проверим"

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=kbs.check_access(),
    )


def available_orders(context, chat_id, prev_message_id, orders):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    text = "Доступные заказы"

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=kbs.available_orders(orders),
    )


def orders(context, chat_id, prev_message_id, orders):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    text = "Current orders:"  # TODO change text

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=kbs.orders(orders),
    )


def stats(context, chat_id, prev_message_id):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    text = "You are breathtaking"

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=kbs.BACK,
    )


def order_detail_public(context, chat_id, order_id, prev_message_id=None):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    order_puplic_detail = storage.get_order_public_detail(order_id)

    context.bot.send_message(
        chat_id=chat_id,
        text=order_puplic_detail,
        reply_markup=kbs.available_order_actions(order_id),
    )


def order_detail_full(
    context, chat_id, order_id, prev_message_id=None, with_keyboard=True
):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    full_detail = storage.get_order_full_detail(order_id)

    context.bot.send_message(
        chat_id=chat_id,
        text=full_detail,
        reply_markup=kbs.order_actions(order_id) if with_keyboard else None,
    )


def time_estimate_request(context, chat_id, prev_message_id, order_id):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    text = f"Введите временную оценку для заказа #{order_id} в днях"

    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=kbs.BACK,
    )


def order_report_request(context, chat_id, order_id, prev_message_id=None):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    context.bot.send_message(
        chat_id=chat_id,
        text=f"Введите отчет для заказа #{order_id}",
        reply_markup=kbs.BACK,
    )


def order_complete_confirmation(context, chat_id, order_id, prev_message_id=None):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    context.bot.send_message(
        chat_id=chat_id,
        text=f"Подтвердите завершение заказа #{order_id}",
        reply_markup=kbs.order_compete_confirmation(),
    )


def order_completed(context, chat_id, order_id, prev_message_id=None):
    if prev_message_id:
        context.bot.delete_message(chat_id=chat_id, message_id=prev_message_id)

    context.bot.send_message(
        chat_id=chat_id,
        text=f"Заказ #{order_id} закрыт.",
    )
