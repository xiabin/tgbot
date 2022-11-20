"""
    Telegram event handlers
"""
from telegram.ext import (
    CommandHandler, MessageHandler, Filters,
)

from tgbot.handlers import fy, message, error


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler("fy", fy))
    dp.add_handler(
        MessageHandler((Filters.text | Filters.voice | Filters.sticker | Filters.audio) & (~Filters.command), message))
    dp.add_error_handler(error)

    return dp
