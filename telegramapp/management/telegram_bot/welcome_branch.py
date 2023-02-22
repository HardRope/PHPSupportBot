from textwrap import dedent

from .telegram_keyboards.welcome_keyboards import (
    get_role_choosing_menu,
    get_client_agreement_menu,
    get_send_resume_menu,
    get_back_menu,
    get_check_status_menu,
    get_main_menu,
)


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


def send_contractor_info(context, chat_id, message_id):
    message_text = 'Тут информация для подрядчиков'
    context.bot.send_message(
        chat_id=chat_id,
        text=dedent(message_text),
        reply_markup=get_send_resume_menu()
    )

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id
    )


def start(update, context):
    # TODO: проверка роли пользователя

    if update.message:
        chat_id=update.message.chat_id
        message_id=update.message.message_id
    elif update.callback_query:
        chat_id = update.callback_query.message.chat_id
        message_id=update.callback_query.message.message_id
    else:
        return

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
        send_contractor_info(context, chat_id, message_id)
        return 'REQUEST_RESUME'


def client_confirmation_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'agree':
        # TODO: создание client'a
        return 'MAIN_MENU'
    elif query.data == 'back':
        send_start_message(context, chat_id, message_id)
        return 'ROLE'


def request_contractor_resume_handler(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    if query.data == 'back':
        send_start_message(context, chat_id, message_id)
        return 'ROLE'

    elif query.data == 'send_resume':
        message_text = 'Отправьте нам небольшое текстовое описание себя'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_back_menu(),
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'GET_RESUME'


def get_resume_handler(update, context):
    query = update.callback_query
    if update.message:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    elif query:
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

    if query and query.data == 'back':
        send_contractor_info(context, chat_id, message_id)
        return 'REQUEST_RESUME'
    else:
        # TODO: создать contractor'а, отправить резюме
        contractor_resume = update.message.text

        message_text = 'Ваша заявка принята, зайдите позже, чтобы проверить статус заявки'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_check_status_menu(),
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CHECK_STATUS'


def check_status_handler(update, context):
    # TODO: проверка статуса contractor'a
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    status = False

    if status == True:
        message_text = 'Вы успешно авторизованы!'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_main_menu(),
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'MAIN_MENU'
    elif status == False:
        message_text = 'Заявка ещё находится на рассмотрении'
        context.bot.send_message(
            chat_id=chat_id,
            text=dedent(message_text),
            reply_markup=get_check_status_menu(),
        )

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
        return 'CHECK_STATUS'


def main_menu_handler(update, context):
    pass
