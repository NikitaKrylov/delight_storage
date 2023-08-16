from dataclasses import asdict
from typing import Callable, Iterable
from accounts.services.models import NotificationData
from celerycore.tasks import send_notifications


def notify(nt: NotificationData, send_type: Callable):
    if not callable(send_type):
        raise TypeError("send_type must be callable")

    send_type(nt)


def MODEL_SEND_BY_CELERY(nt: NotificationData):
    send_notifications.delay(asdict(nt))


def MODEL_SEND(nt: NotificationData):
    send_notifications(asdict(nt))


def EMAIL_SEND(nt: NotificationData): ...


def EMAIL_SEND_BY_CELERY(nt: NotificationData): ...

