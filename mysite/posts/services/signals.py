from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from celerycore.tasks import send_notifications
from posts.models import Post, Comment
from accounts.models import Notification


@receiver(models.signals.post_save, sender=Post)
def notify_on_post_saved(sender, instance: Post, created: bool, raw, using, update_fields, **kwargs):
    if not instance: return

    if (update_fields is not None and 'status' in update_fields) or created:
        if instance.status == Post.STATUS.PUBLISHED:
            # send_notifications.delay(
            #     recipient_ids=list(instance.author.user_subscriptions.filter(status=1).values_list('subscriber__id', flat=True)),
            #     sender_id=instance.author.id,
            #     n_type=Notification.Types.NEW_POST,
            #     verb=_("Новый пост от {}".format(instance.author)),
            #     message=_('Смотреть новый <a style="color: #DCA1F5; text-decoration: underline;" href="{}">пост</a>'.format(
            #             reverse('post', kwargs={'pk': instance.pk}))),

            # )
            pass


@receiver(models.signals.post_save, sender=Comment)
def notify_on_comment_replied(sender, instance: Comment, created: bool, raw, using, update_fields, **kwargs):
    if not instance:return

    if instance.author == instance.post.author and instance.answered is None: return

    if created and instance.answered:
        # send_notifications.delay(
        #     sender_id=instance.author.id,
        #     recipient_ids=[instance.answered.author.id],
        #     verb="Ответ на комментарий",
        #     n_type=Notification.Types.COMMENT,
        #     message='{author} ответил на ваш комментарий под <a style="color: #DCA1F5; text-decoration: underline;" href="{url}">постом {id}</a>'.format(
        #         author=instance.author.username,
        #         url=reverse('post', kwargs={'pk': instance.post.pk}),
        #         id=instance.post.id
        #     )

        # )
        pass
    elif created and not instance.answered:
        # send_notifications.delay(
        #     sender_id=instance.author.id,
        #     recipient_ids=[instance.post.author.id],
        #     verb="Новый комментарий",
        #     n_type=Notification.Types.COMMENT,
        #     message='{author} прокомментировал ваш <a style="color: #DCA1F5; text-decoration: underline;" href="{url}">пост {id}</a>'.format(
        #         author=instance.author.username,
        #         url=reverse('post', kwargs={'pk': instance.post.pk}),
        #         id=instance.post.id
        #     )

        # )
        pass
