import asyncio
import datetime
import logging
import time
from asyncio import Task

from asgiref.sync import sync_to_async
from celery.app import task
from django.core.management import BaseCommand
from django.utils import timezone

from tgbot.models.messages import Message, getCount
from tgbot.tasks import add, mul


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        add.apply_async((4, 3), countdown=10)
        mul.delay(4, 3)
        pass
