from django.core.management import BaseCommand
from telegram import Bot
from telegram.ext import Updater

from tgbot.dispatcher import setup_dispatcher
from tgbot.settings import TELEGRAM_TOKEN


class Command(BaseCommand):
    help = '运行Telegram 机器人'

    def handle(self, *args, **options):
        updater = Updater(TELEGRAM_TOKEN, use_context=True)
        setup_dispatcher(updater.dispatcher)
        tgbot_info = Bot(TELEGRAM_TOKEN).get_me()
        tgbot_link = f"https://t.me/{tgbot_info['username']}"
        self.stdout.write(f"Polling of '{tgbot_link}' has started")
        updater.start_polling()
        updater.idle()
