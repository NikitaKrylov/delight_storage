from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from .models import PostComplaint, Notification


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(models.signals.post_save, sender=PostComplaint)
def notify_on_post_complaint_created(sender, instance: PostComplaint, created: bool, raw, using, update_fields, **kwargs):
    if instance is None: return

    if created:
        Notification.objects.create(
            actor=instance.sender,
            recipient=instance.post.author,
            verb="Жалоба на пост".format(),
            action_object=instance,
            target=instance.post,
            type=Notification.Types.COMPLAINT,
            description="""
            Пользователь {name} оставил жалобу на <a style="color: #DCA1F5; text-decoration: underline;" href="{post_url}">{post_name}</a>
            <p><b>Тип:</b> {c_type}</p>
            <p><b>Описание:</b> {c_desc}</p>
            <a style="color: #DCA1F5; text-decoration: none;" href="#">Смотреть подробнее</a>
            """.format(
                name=instance.sender,
                post_name=str(instance.post),
                c_type=instance.type,
                c_desc=instance.description,
                post_url=reverse('post', kwargs={'pk': instance.pk}))


        )


