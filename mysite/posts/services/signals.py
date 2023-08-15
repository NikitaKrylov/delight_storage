from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from celerycore.tasks import send_notifications
from mysite.settings import USE_CELERY
from posts.models import Post, Comment
from accounts.models import Notification, NotificationData


@receiver(models.signals.post_save, sender=Post)
def notify_on_post_saved(
        sender, instance: Post, created: bool, raw, using, update_fields, **kwargs
):
    print(instance, update_fields, instance.status == Post.STATUS.PUBLISHED)
    if not instance:
        return

    if (update_fields is not None and "status" in update_fields) or created:
        if instance.status == Post.STATUS.PUBLISHED:
            nd = dict(
                recipient_ids=list(
                    instance.author.user_subscriptions.filter(status=1).values_list(
                        "subscriber__id", flat=True
                    )
                ),
                sender_id=instance.author.id,
                n_type=Notification.Types.NEW_POST,
                verb=_("Новый пост от {}".format(instance.author)),
                message=_(
                    'Смотреть новый <a style="color: #DCA1F5; text-decoration: underline;" href="{}">пост</a>'.format(
                        reverse("post", kwargs={"pk": instance.pk})
                    )
                )
            )

            if USE_CELERY:
                send_notifications.delay(nd)
                print("send use celery")

            else:
                send_notifications(nd)
                print("send without celery")


@receiver(models.signals.post_save, sender=Comment)
def notify_on_comment_replied(
        sender, instance: Comment, created: bool, raw, using, update_fields, **kwargs
):
    if not instance:
        return

    # если комментарий пренадлежит автору поста
    if instance.author == instance.post.author and instance.answered is None:
        return

    # если данные валидны, но уведомления отключены
    if not ((instance.answered and instance.answered.author.settings.notify_on_comment_reply) or (
            (not instance.answered) and instance.post.author.settings.notify_on_post_commented)):
        return

    url = reverse("post", kwargs={"pk": instance.post.pk})
    username = instance.author.username
    post_id = instance.post.id
    nd = dict(
        sender_id=instance.author.id,
        recipient_ids=[instance.answered.author.id],
        verb="Ответ на комментарий" if instance.answered else "Новый комментарий",
        n_type=Notification.Types.COMMENT,
        message=
        f'{username} ответил на ваш комментарий под <a style="color: #DCA1F5; text-decoration: underline;" href="{url}">постом {post_id}</a>'
        if instance.answered
        else f'{username} прокомментировал ваш <a style="color: #DCA1F5; text-decoration: underline;" href="{url}">пост {post_id}</a>'
    )

    if USE_CELERY:
        send_notifications.delay(nd)
    else:
        send_notifications(nd)
