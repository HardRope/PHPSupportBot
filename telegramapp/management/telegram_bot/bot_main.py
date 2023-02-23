import logging
from functools import partial
from django.conf import settings

import redis
from telegram.ext import (
    Filters,
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    # PreCheckoutQueryHandler,
)

from .welcome_branch import (
    start,
    confirm_role_handler,
    client_confirmation_handler,
    request_contractor_resume_handler,
    get_resume_handler,
    check_status_handler,
)

from .client_branch import (
    client_main_menu_handler,
    create_order_handler,
    create_ticket_handler,
    active_orders_handler,
    complete_orders_handler,
    get_order_handler,
    tariffs_handler,
    tariff_handler,
)

logger = logging.getLogger(__name__)


def error(state, error):
    logger.warning(f'State {state} caused error {error}')


def handle_users_reply(update, context, db):
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
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
        'REQUEST_RESUME': request_contractor_resume_handler,
        'GET_RESUME': get_resume_handler,
        'CHECK_STATUS': check_status_handler,
        'CONFIRMATION': client_confirmation_handler,

        # Client states
        'CLIENT_MAIN_MENU': client_main_menu_handler,
        'CREATE_ORDER': create_order_handler,
        'CREATE_TICKET': create_ticket_handler,
        'CLIENT_ACTIVE_ORDERS': active_orders_handler,
        'CLIENT_COMPLETE_ORDERS': complete_orders_handler,
        'CLIENT_ORDER': partial(get_order_handler, db=db),
        'TARIFFS': tariffs_handler,
        'TARIFF': tariff_handler,

        # Payment states
        'PAYMENT': None,

        # Contractor states
        'GET_MESSAGE': None,
        # Manager states
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

    dispatcher.add_handler(CallbackQueryHandler(handler_connected_db))
    dispatcher.add_handler(MessageHandler(Filters.text, handler_connected_db))
    dispatcher.add_handler(CommandHandler('start', handler_connected_db))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
