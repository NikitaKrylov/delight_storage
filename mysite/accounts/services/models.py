from dataclasses import dataclass
from typing import List

from accounts.models import Notification


@dataclass(frozen=True)
class NotificationData:
    sender_id: int
    recipient_ids: List[int]
    verb: str
    message: str
    n_type: Notification.Types

