from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_client_main_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Создать заявку', callback_data='create')],
        [InlineKeyboardButton('Заказы в работе', callback_data='active')],
        [InlineKeyboardButton('Выполненные заказы', callback_data='complete')],
        [InlineKeyboardButton('Тарифы', callback_data='tariffs')],
        [InlineKeyboardButton('Связь с менеджером', callback_data='ticket')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_back_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_active_orders_menu():
    # TODO: список активных заказов клиента -> id
    inline_keyboard = [[InlineKeyboardButton(f'Заказ {id}', callback_data=id)] for id in range(3)]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_complete_orders_menu():
    #TODO: список выполненных заказов клиента -> id

    inline_keyboard = [[InlineKeyboardButton(f'Заказ {id}', callback_data=id)] for id in range(3)]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_order_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Связь с менеджером', callback_data='ticket')],
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_tariffs_menu():
    # TODO: список тарифов -> name
    inline_keyboard = [[InlineKeyboardButton(f'Тариф {name}', callback_data=name)] for name in range(3)]
    inline_keyboard += [
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup


def get_tariff_menu():
    inline_keyboard = [
        [InlineKeyboardButton('Купить', callback_data='buy')],
        [InlineKeyboardButton('Назад', callback_data='back')],
    ]
    inline_kb_markup = InlineKeyboardMarkup(inline_keyboard)

    return inline_kb_markup
