from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def new_ticket_menu(ticket_id):
    inline_keyboard = [
        [InlineKeyboardButton('Принять заявку', callback_data='read')],
        [InlineKeyboardButton('Пропустить', callback_data=ticket_id)],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup
