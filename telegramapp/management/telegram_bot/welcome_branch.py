from textwrap import dedent

from .telegram_keyboards.welcome_keyboards import (
    get_role_choosing_menu,
    get_client_agreement_menu,
    get_back_menu,
    get_check_status_menu,
)
from .client_branch import send_client_main_menu
from .manager_branch import send_manager_main_menu
from .db_requests.welcome_db_requests import (
    check_user_role,
    get_or_create_user,
    create_client
)

from . import contractors


def send_start_message(context, chat_id, message_id):
    message_text = 'Добро пожаловать в PHPSupportBot'

    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_role_choosing_menu()
    )
    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def start(update, context):
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
        tg_username = update.message.chat.username
        get_or_create_user(chat_id, tg_username)
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id
        message_id=update.callback_query.message.message_id
    else:
        return

    role = check_user_role(chat_id)
    if role:
        if role == 'client':
            send_client_main_menu(context, chat_id, message_id)
            return 'CLIENT_MAIN_MENU'
        if role == 'manager':
            send_manager_main_menu(context, chat_id, message_id)
            return 'MANAGER_MAIN_MENU'
        if role == 'contractor':
            return contractors.entrypoint_with_role(context, chat_id, message_id)

    send_start_message(context, chat_id, message_id)
    return 'ROLE'


def confirm_role_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'client':
        message_text = 'Тут должно быть пользовательское соглашение'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_client_agreement_menu()
        )
        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CONFIRMATION'

    elif query.data == 'contractor':
        return contractors.entrypoint_with_no_role(context, chat_id, message_id)


def client_confirmation_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    tg_username = query.message.chat.username

    if query.data == 'agree':
        create_client(chat_id, tg_username)
        send_client_main_menu(context, chat_id, message_id)
        return 'CLIENT_MAIN_MENU'
    elif query.data == 'back':
        send_start_message(context, chat_id, message_id)
        return 'ROLE'

