from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from .models import Post, Comment
from accounts.services import get_client_ip
from accounts.models import ClientIP, Notification


def update_post_views(request, post: Post):
    if post is None: return
    user = request.user

    if user.is_authenticated:
        user_view, created = post.views.get_or_create(user=user)
    else:
        clien_ip, ip_created = ClientIP.objects.get_or_create(ip=get_client_ip(request))
        user_view, created = post.views.get_or_create(client_ip=clien_ip)


@receiver(models.signals.post_save, sender=Post)
def notify_on_post_saved(sender, instance: Post, created: bool, raw, using, update_fields, **kwargs):
    if not instance: return

    if (update_fields is not None and 'status' in update_fields) or created:
        if instance.status == Post.STATUS.PUBLISHED:
            for sub in instance.author.user_subscriptions.filter(status=1):
                Notification.objects.create(
                    actor=instance.author,
                    recipient=sub.subscriber,
                    verb="Новый пост от {}".format(instance.author),
                    action_object=instance,
                    target=instance,
                    type=Notification.Types.NEW_POST,
                    description='Смотреть новый <a style="color: #DCA1F5; text-decoration: underline;" href="{}">пост</a>'.format(
                        reverse('post', kwargs={'pk': instance.pk}))
                )


@receiver(models.signals.post_save, sender=Comment)
def notify_on_comment_replied(sender, instance: Comment, created: bool, raw, using, update_fields, **kwargs):
    if not instance:return

    if instance.author == instance.post.author: return

    if created and instance.answered:
        Notification.objects.create(
            actor=instance.author,
            recipient=instance.answered.author,
            verb="Ответ на комментарий",
            action_object=instance,
            target=instance,
            type=Notification.Types.COMMENT,
            description='{author} ответил на ваш комментарий под <a style="color: #DCA1F5; text-decoration: underline;" href="{url}">постом {id}</a>'.format(
                author=instance.author.username,
                url=reverse('post', kwargs={'pk': instance.post.pk}),
                id=instance.post.id
            )

        )
    elif created and not instance.answered:
        Notification.objects.create(
            actor=instance.author,
            recipient=instance.post.author,
            verb="Новый комментарий",
            action_object=instance,
            target=instance,
            type=Notification.Types.COMMENT,
            description='{author} прокомментировал ваш <a style="color: #DCA1F5; text-decoration: underline;" href="{url}">пост {id}</a>'.format(
                author=instance.author.username,
                url=reverse('post', kwargs={'pk': instance.post.pk}),
                id=instance.post.id
            )

        )


