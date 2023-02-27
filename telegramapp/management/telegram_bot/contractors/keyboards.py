from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def _create_keyboard(keyboard_blueprint, with_back=False, with_home=False):
    """Creates InlineKeyboardMarkup from a blueprint like:
    {
        "read": "Прочитано",
        "ORDER_ID": "Ответить сразу",
    }
    """
    if with_back:
        keyboard_blueprint["back"] = "Назад"

    if with_home:
        keyboard_blueprint["home"] = "Главное меню"

    inline_keyboard = [
        [InlineKeyboardButton(label, callback_data=callback_data)]
        for callback_data, label in keyboard_blueprint.items()
    ]

    return InlineKeyboardMarkup(inline_keyboard)


BACK = _create_keyboard({}, with_back=True)

TO_HOME = _create_keyboard({}, with_home=True)


def check_access():
    return _create_keyboard({"check": "Проверить статус"})


def home():
    return _create_keyboard(
        {
            "available_orders": "Новые заказы",
            "current_orders": "Текущие заказы",
            "stats": "Статистика",
        }
    )


def incoming_message(order_id: int):
    return _create_keyboard(
        {
            "read": "Прочитано",
            order_id: "Ответить сразу",
        }
    )


def available_orders(order_ids):
    """
    Assuming orders == [1,2,3]
    """
    return _create_keyboard(
        {order.id: f"Новый заказ #{order.id}" for order in order_ids}, with_back=True
    )


def available_order_actions(order_id):
    """
    Assuming orders == [1,2,3]
    """
    return _create_keyboard(
        {
            f"take_{order_id}": f"Взять заказ",
        },
        with_back=True,
    )


def orders(order_ids):
    """
    Assuming orders == [1,2,3]
    """
    return _create_keyboard(
        {order.id: f"Заказ #{order.id}" for order in orders},
        with_back=True,
    )


def order_actions(order_id):
    """
    Assuming orders == [1,2,3]
    """
    return _create_keyboard(
        {
            f"complete_{order_id}": f"Завершить заказ",
        },
        with_back=True,
    )


def order_compete_confirmation():
    return _create_keyboard(
        {
            "yes": "Да",
            "no": "Нет",
        },
    )
