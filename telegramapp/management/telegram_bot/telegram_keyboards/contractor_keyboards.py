from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def new_message_menu(order_id):
    inline_keyboard = [
        [InlineKeyboardButton('Прочитано', callback_data='read')],
        [InlineKeyboardButton('Ответить сразу', callback_data=order_id)],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup
