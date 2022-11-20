import logging

from celery import shared_task
from telegram import Bot

from tgbot.celery import app
from tgbot.settings import TELEGRAM_TOKEN


@shared_task(ignore_result=True)
def mul(x, y):
    logging.info("mul 执行")
    return x * y


@shared_task(ignore_result=True)
def add(x, y):
    logging.info("add 执行")
    return x + y


@app.task(ignore_result=True)
def delete_message(chat_id, message_id):
    logging.info('删除信息开始')
    Bot(TELEGRAM_TOKEN).delete_message(chat_id, message_id)
    logging.info('删除信息完成')
