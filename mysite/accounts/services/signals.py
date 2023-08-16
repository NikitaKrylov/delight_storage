from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from accounts.models import PostComplaint, Notification, UserSettings, User
from accounts.services.models import NotificationData
from accounts.services.notifications import notify, MODEL_SEND, MODEL_SEND_BY_CELERY
from mysite.settings import USE_CELERY


@receiver(models.signals.post_save, sender=User)
def create_user_settings_on_user_created(sender, instance: User, created: bool, raw, using, update_fields, **kwargs):
    if created:
        UserSettings.objects.create(
            user=instance
        )


@receiver(models.signals.post_save, sender=PostComplaint)
def notify_on_post_complaint_created(sender, instance: PostComplaint, created: bool, raw, using, update_fields,
                                     **kwargs):
    if instance is None: return

    if created:
        nd = NotificationData(
            sender_id=instance.sender.id,
            recipient_ids=[instance.post.author.id],
            verb="Жалоба на пост".format(),
            n_type=Notification.Types.COMPLAINT,
            message="""
            Пользователь {name} оставил жалобу на <a style="color: #DCA1F5; text-decoration: underline;" href="{post_url}">{post_name}</a>
            <p><b>Тип:</b> {c_type}</p>
            <p><b>Описание:</b> {c_desc}</p>
            <a style="color: #DCA1F5; text-decoration: none;" href="#">Смотреть подробнее</a>
            """.format(
                name=instance.sender,
                post_name=str(instance.post),
                c_type=instance.get_type_display(),
                c_desc=instance.description,
                post_url=instance.post.get_absolute_url())

        )
        notify(nd, MODEL_SEND_BY_CELERY if USE_CELERY else MODEL_SEND)
