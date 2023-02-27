import logging

from .client_branch import send_tariffs, send_client_main_menu


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
        return 'TARIFFS'


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
    chat_id = user.id

    message_text = f'Вы оплатили тариф {tariff.get("name")}. Приятного пользования нашим сервисом. '
    send_client_main_menu(context, chat_id, message_id, message_text)
    return 'CLIENT_MAIN_MENU'
