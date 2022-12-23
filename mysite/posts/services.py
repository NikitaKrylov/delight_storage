from django.urls import reverse

from .models import Post
from accounts.services import get_client_ip
from accounts.models import ClientIP
from django.dispatch import receiver
from django.db import models
from accounts.models import Notification


def update_post_views(request, post: Post):
    if post is None: return
    user = request.user

    if user.is_authenticated:
        user_view, created = post.views.get_or_create(user=user)
    else:
        clien_ip, ip_created = ClientIP.objects.get_or_create(ip=get_client_ip(request))
        user_view, created = post.views.get_or_create(client_ip=clien_ip)


@receiver(models.signals.post_save, sender=Post)
def notify_on_post_saved(sender, instance: Post, **kwargs):
    if not instance: return

    if kwargs['update_fields'] and 'status' in kwargs['update_fields']:
        if instance.status == Post.STATUS.PUBLISHED:
            for sub in instance.author.user_subscriptions.filter(status=1):
                Notification.objects.create(
                            actor=instance.author,
                            recipient=sub.subscriber,
                            verb="Новый пост от {}".format(instance.author),
                            action_object=instance,
                            target=instance,
                            type=Notification.Types.NEW_POST,
                            description='Смотреть новый <a style="color: #DCA1F5; text-decoration: underline;" href="{}">пост</a>'.format(reverse('post', kwargs={'pk': instance.pk}))
                )

