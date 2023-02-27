import logging

from .client_branch import send_tariffs, send_client_main_menu
from .db_requests.payments_requests import create_subscription


logger = logging.getLogger(__name__)

def payment_handler(update, context):
    bool(update.pre_checkout_query)
    if update.callback_query:
        query = update.callback_query
        if query.data == 'back':
            chat_id = query.message.chat_id
            message_id = query.message.message_id
            send_tariffs(context, chat_id, message_id)
            return 'TARIFFS'
    elif update.pre_checkout_query:
        precheckout_callback(update, context)
        return 'PAYMENT'
    else:
        successful_payment_callback(update, context)
        return 'CLIENT_MAIN_MENU'


def precheckout_callback(update, context):
    query = update.pre_checkout_query
    chat_id = query.from_user.id
    logger.info("Payload %s - precheckout_callback", query.invoice_payload)
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)


def successful_payment_callback(update, context):
    tariff = context.user_data['choosing_tariff']
    user = update.message.from_user
    message_id = update.message.message_id
    logger.info("User %s made a payment for %s rubles", user.first_name, tariff.get("price"))
    is_subscription_created = create_subscription(user.id, tariff.get('tariff_name'))

    message_text = f'Вы оплатили тариф {tariff.get("tariff_name")}. Приятного пользования нашим сервисом. '
    if not is_subscription_created:
        message_text = 'Что-то пошло не так. Обратитесь к администратору'

    send_client_main_menu(context, user.id, message_id, message_text)
