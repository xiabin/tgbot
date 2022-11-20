import datetime
import logging

from django.core.cache import cache
from django.db import models
from django.utils import timezone


class Message(models.Model):
    sender_chat_id = models.BigIntegerField()
    id = models.IntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    message_thread_id = models.BigIntegerField()
    date = models.DateTimeField()

    class Meta:
        db_table = 't_message'


def getCount(sender_chat_id: int, user_id: int, model: int) -> int:
    key = f"count::{sender_chat_id}::{user_id}::{model}"
    count = cache.get(key)
    if count is None:
        if model == 1:
            query = Message.objects.filter(sender_chat_id=sender_chat_id, user_id=user_id,
                                           date__gte=timezone.now().replace(hour=0, minute=0, second=0, microsecond=0))
            pass
        elif model == 2:
            end = timezone.now()
            start = end - datetime.timedelta(days=7)
            query = Message.objects.filter(sender_chat_id=sender_chat_id, user_id=user_id,
                                           date__range=(start, end))
            pass
        elif model == 3:
            end = timezone.now()
            start = end - datetime.timedelta(days=30)
            query = Message.objects.filter(sender_chat_id=sender_chat_id, user_id=user_id,
                                           date__range=(start, end))
            cache.set(key, count, 60)
        return query.count()
    else:
        return count
