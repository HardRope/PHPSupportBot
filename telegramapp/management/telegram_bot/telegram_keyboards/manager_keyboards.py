from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_back_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def new_ticket_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Прочитано', callback_data='miss')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def manager_main_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Необработанные тикеты', callback_data='tickets')],
        [InlineKeyboardButton('Мои заявки', callback_data='manager_tickets')],
        [InlineKeyboardButton('Активные заказы', callback_data='orders')],
        [InlineKeyboardButton('Свободные исполнители', callback_data='contractors')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def tickets_menu(tickets):
    inline_keyboard = [[InlineKeyboardButton(f'Заявка №{id}', callback_data=id)] for id in tickets]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def ticket_menu(ticket_id):
    inline_keyboard = [
        [InlineKeyboardButton('Принять заявку', callback_data=ticket_id)],
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def active_orders_menu(orders):
    inline_keyboard = [[InlineKeyboardButton(f'Заказ №{id}', callback_data=id)] for id in orders]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def free_contractors_menu(contractors):
    inline_keyboard = [[InlineKeyboardButton(f'{contractor.get("username")}', callback_data=contractor.get("tg_id"))] for contractor in contractors]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup