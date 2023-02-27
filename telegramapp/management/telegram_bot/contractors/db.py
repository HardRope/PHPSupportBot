from django.core.exceptions import ObjectDoesNotExist

from orderapp.models import Contractor
from telegramapp.management.telegram_bot.db_requests.welcome_db_requests import (
    get_or_create_user,
)

# TODO: проверка статуса контрактора (авторизован/неавторизован) -> True, False
def is_active(tg_chat_id):
    try:
        contractor = Contractor.objects.get(user__tg_chat_id=tg_chat_id)
        if not contractor.active:
            return False
        return True
    except ObjectDoesNotExist:
        return False


# TODO: создание контрактора -> None
def create_contractor(tg_chat_id, tg_username, resume, username=None):
    user = get_or_create_user(tg_chat_id, tg_username, username)
    contractor, created = Contractor.objects.get_or_create(user=user, resume=resume)
