import json
import logging
import traceback
from pydoc import html

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from tgbot.models.messages import getCount, Message
from tgbot.settings import TELEGRAM_LOGS_CHAT_ID
from tgbot.tasks import delete_message

logger = logging.getLogger(__name__)


def fy(update: Update, context: CallbackContext):
    logger.info(f'消息是:{update.message.to_json()}')
    day = getCount(update.effective_chat.id, update.message.from_user.id, 1)
    week = getCount(update.effective_chat.id, update.message.from_user.id, 2)
    month = getCount(update.effective_chat.id, update.message.from_user.id, 3)
    text = f"@{update.message.from_user.username} 你好！{update.message.from_user.full_name}, 发言数如下(数据有1分钟延迟)：\n" \
           f"1. 当天发言：{day} 条\n" \
           f"2. 7 天内发言：{week} 条\n" \
           f"3. 30 天内发言：{month} 条 \n"
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    delete_message.apply_async((update.effective_chat.id, update.message.message_id))
    delete_message.apply_async((update.effective_chat.id, message.message_id), countdown=8)


def message(update: Update, context: CallbackContext):
    logger.info(f'消息是:{update.message.to_json()}')
    message = Message(sender_chat_id=update.effective_chat.id, user_id=update.message.from_user.id,
                      message_thread_id=None, date=update.message.date,
                      id=update.message.message_id)
    message.save()


def error(update: object, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    context.bot.send_message(
        chat_id=TELEGRAM_LOGS_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )
