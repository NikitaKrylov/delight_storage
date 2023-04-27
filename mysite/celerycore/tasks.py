from typing import List

from django.utils import timezone

from accounts.models import Notification, User
from posts.models import Post
from celery import shared_task
from . import celery_app


@celery_app.task
def publish_posts():
    posts = list(Post.objects.filter(status=Post.STATUS.DEFERRED).filter(delayed_publication_time__lte=timezone.now()))

    for post in posts:
        post.status = Post.STATUS.PUBLISHED
        post.pub_date = post.delayed_publication_time
        post.delayed_publication_time = None
        post.save(update_fields=['status', 'pub_date', 'delayed_publication_time'])


@shared_task
def parse_image_from_source():
    pass


@shared_task
def send_notifications(recipient_ids: List[int], sender_id: int, n_type: Notification.Types, verb: str, message: str = "", action_object=None):
    from accounts.models import Notification, User

    actor = User.objects.get(id=sender_id)
    subs = [subscriber for subscriber in User.objects.filter(id__in=recipient_ids).all()]
    nt = [Notification(
        actor=actor,
        recipient=subscriber,
        verb=verb,
        action_object=action_object,
        target=action_object,
        type=n_type,
        description=message
    ) for subscriber in subs]
    Notification.objects.bulk_create(nt)
    return len(subs)


