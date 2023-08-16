from django.test import TestCase
import random
from string import ascii_uppercase
from dataclasses import asdict
from accounts.models import Notification
from accounts.services.models import NotificationData


class NotificationTestCase(TestCase):

    def test_notification_dataclass_serializable(self):
        data = [dict(
        sender_id=random.randint(1, 1000),
        recipient_ids=[random.randint(1, 1000) for i in range(random.randint(1, 100))],
        verb=''.join(random.choices(ascii_uppercase, k=random.randint(1, 100))),
        n_type=Notification.Types.COMMENT,
        message=''.join(random.choices(ascii_uppercase, k=random.randint(1, 100)))
    ) for i in range(100)]
        nts = [NotificationData(**d) for d in data]

        for d1, d2 in zip(data, nts):
            self.assertDictEqual(d1, asdict(d2))

