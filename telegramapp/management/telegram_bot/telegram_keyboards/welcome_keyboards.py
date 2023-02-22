from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_role_choosing_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Заказчик', callback_data='client')],
        [InlineKeyboardButton('Исполнитель', callback_data='contractor')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_client_agreement_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Согласиться', callback_data='agree')],
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_send_resume_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Отправить резюме', callback_data='send_resume')],
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_back_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_check_status_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Проверить статус', callback_data='checl')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_main_menu():
    inline_keyboard = [
        [InlineKeyboardButton('В главное меню', callback_data='main_menu')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup
