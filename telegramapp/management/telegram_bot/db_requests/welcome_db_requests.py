from django.core.exceptions import ObjectDoesNotExist
from orderapp.models import Person, Contractor, Client, Manager, Order, Ticket, Subscription


#TODO: проверка роли пользователя (менеджер, контрактор, клиент) -> str
def check_user_role(tg_chat_id):
    try:
        user = Person.objects.get(tg_chat_id=tg_chat_id)
        if hasattr(user, 'client'):
            return 'client'
        elif hasattr(user, 'manager'):
            return 'manager'
        elif hasattr(user, 'contractor'):
            return 'contractor'
        else:
            return None
    except ObjectDoesNotExist:
        return None
    

def get_or_create_user(tg_chat_id, tg_username, username=None):
    username = tg_username if not username else username
    user, created = Person.objects.get_or_create(tg_chat_id=tg_chat_id,
                                                 tg_username=tg_username,
                                                 username=username,
                                                 password=tg_chat_id)
    return user



#TODO: создание клиента -> None
def create_client(tg_chat_id, tg_username, username=None):
    user = get_or_create_user(tg_chat_id, tg_username, username)
    client, created = Client.objects.get_or_create(user=user)
    return


#TODO:

#TODO:

#TODO:
