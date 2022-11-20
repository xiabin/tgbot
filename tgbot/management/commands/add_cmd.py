import logging
from typing import Dict

from django.core.management import BaseCommand
from telegram import Bot, BotCommand
from telegram.ext import Updater

from tgbot.dispatcher import setup_dispatcher
from tgbot.settings import TELEGRAM_TOKEN


class Command(BaseCommand):
    help = ' 添加命令'

    def handle(self, *args, **options):
        logging.info(123);
        # langs_with_commands: Dict[str, Dict[str, str]] = {
        #     'en': {
        #         'fy': '查询发言 🙋',
        #     }
        # }
        # Bot.delete_my_commands(Bot)
        # for language_code in langs_with_commands:
        #     Bot.set_my_commands(
        #         language_code=language_code,
        #         commands=[
        #             BotCommand(command, description) for command, description in
        #             langs_with_commands[language_code].items()
        #         ]
        #     )
