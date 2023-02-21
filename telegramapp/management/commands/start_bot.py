from django.core.management.base import BaseCommand

from telegramapp.management.telegram_bot.bot_main import main


class Command(BaseCommand):
    help = 'Start bot'

    def handle(self, *args, **options):
        main()
