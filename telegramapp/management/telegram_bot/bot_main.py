import logging
from functools import partial
from django.conf import settings

import redis
from telegram.ext import (
    # Filters,
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    # MessageHandler,
    # PreCheckoutQueryHandler,
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
        # Client states
        
        # Contractor states
        
        # Manager states
    }

    print(user_state)
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(context, update)
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
    dispatcher.add_handler(CommandHandler('start', handler_connected_db))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
