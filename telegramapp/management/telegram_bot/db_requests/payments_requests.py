from django.core.exceptions import ObjectDoesNotExist
from orderapp.models import Person, Contractor, Client, Manager, Order, Ticket, Subscription, Messages
from paymentapp.models import Tariff


def create_subscription(tg_chat_id, tariff_name):
    try:
        client = Client.objects.get(user__tg_chat_id=tg_chat_id)
        tariff = Tariff.objects.get(name=tariff_name)
        subscription, created = Subscription.objects.get_or_create(
            client=client,
            tariff=tariff,
        )
        if not created:
            subscription.delete()
            Subscription.objects.create(
                client=client,
                tariff=tariff,
            )
        return True
    except ObjectDoesNotExist:
        return False