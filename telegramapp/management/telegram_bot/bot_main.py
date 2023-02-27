import logging
from functools import partial

from django.conf import settings

import redis
from telegram import SuccessfulPayment
from telegram.ext import (
    Filters,
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    PreCheckoutQueryHandler,
)

from .welcome_branch import (
    start,
    confirm_role_handler,
    client_confirmation_handler,
)

from .client_branch import (
    client_main_menu_handler,
    get_task_handler,
    create_ticket_handler,
    active_orders_handler,
    complete_orders_handler,
    get_order_handler,
    tariffs_handler,
    get_credentials_handler,
    client_messages_handler
)

from .manager_branch import (
    manager_main_menu_handler,
    tickets_handler,
    ticket_handler,
    manager_orders_handler,
    free_contractors_handler,
    contractor_contact_handler,
    get_notification_handler,
)
from . import contractors

from .bot_payment import payment_handler

logger = logging.getLogger(__name__)


def error(state, error):
    logger.warning(f'State {state} caused error {error}')
    raise


def handle_users_reply(update, context, db):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    elif update.pre_checkout_query:
        user_reply = None
        chat_id = update.pre_checkout_query.from_user.id
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id)

    states_functions = {
        # Welcome states
        'START': start,
        'ROLE': confirm_role_handler,
        'CONFIRMATION': client_confirmation_handler,

        # Client states
        'CLIENT_MAIN_MENU': client_main_menu_handler,
        'GET_TASK': get_task_handler,
        'GET_CREDENTIALS': get_credentials_handler,
        'CREATE_TICKET': partial(create_ticket_handler, db=db),
        'CLIENT_ACTIVE_ORDERS': active_orders_handler,
        'CLIENT_COMPLETE_ORDERS': complete_orders_handler,
        'CLIENT_ORDER': partial(get_order_handler, db=db),
        'CLIENT_MESSAGES': client_messages_handler,
        'TARIFFS': tariffs_handler,

        'NEW_MESSAGE_TO_CLIENT': None,  # TODO

        # Payment states
        'PAYMENT': payment_handler,

        # Contractor states
        contractors.State.ACCOUNT_ON_REVIEW.value: contractors.handlers.check_access,
        contractors.State.RESUME_REQUEST.value: contractors.handlers.process_resume,
        contractors.State.HOME.value: contractors.handlers.home_actions,

        contractors.State.AVAILABLE_ORDERS.value: contractors.handlers.available_orders_actions,
        contractors.State.AVAILABLE_ORDER_DETAIL.value: partial(contractors.handlers.available_order_detail_actions, db=db),
        contractors.State.TIME_ESTIMATE_REQUEST.value: partial(contractors.handlers.process_time_estimate, db=db),

        contractors.State.ORDERS.value: partial(contractors.handlers.orders_actions, db=db),
        contractors.State.ORDER_DETAIL.value: partial(contractors.handlers.order_detail_actions, db=db),
        contractors.State.ORDER_REPORT_REQUEST.value: partial(contractors.handlers.process_order_report, db=db),
        contractors.State.ORDER_COMPLETE_CONFIRMATION.value: partial(contractors.handlers.order_complete_confirmation_actions, db=db),

        contractors.State.STATISTICS.value: contractors.handlers.stats_actions,

        contractors.State.INCOMING_MESSAGE.value: contractors.handlers.incoming_message_actions,

        # Manager states
        'MANAGER_MAIN_MENU': manager_main_menu_handler,
        'TICKETS': tickets_handler,
        'TICKET_HANDLER': ticket_handler,
        'ACTIVE_ORDERS': manager_orders_handler,
        'FREE_CONTRACTORS': free_contractors_handler,
        'CONTRACTOR_HANDLER': contractor_contact_handler,
        'NOTIFICATION': get_notification_handler,
    }

    print(user_state)                                                   # отладочный принт
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        print(next_state)                                               # отладочный принт
        db.set(chat_id, next_state)
    except Exception as err:
        error(user_state, err)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    tg_token = settings.TELEGRAM_TOKEN
    db = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )
    handler_connected_db = partial(handle_users_reply, db=db)

    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.bot_data = {
        'payment_token': settings.PAYMENT_TOKEN,
    }

    dispatcher.add_handler(MessageHandler(Filters.successful_payment, handler_connected_db))
    dispatcher.add_handler(CallbackQueryHandler(handler_connected_db))
    dispatcher.add_handler(MessageHandler(Filters.text, handler_connected_db))
    dispatcher.add_handler(CommandHandler('start', handler_connected_db))
    dispatcher.add_handler(PreCheckoutQueryHandler(handler_connected_db))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
