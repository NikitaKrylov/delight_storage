from collections import namedtuple
from datetime import datetime, date, timedelta
from typing import List

from django.db.models import QuerySet, Count
from django.dispatch import receiver
from django.db import models
from django.urls import reverse
from .models import PostComplaint, Notification
from posts.models import Post

from posts.models import Comment


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


class ChartStatistic:
    Chart = namedtuple('Chart', 'labels values')

    def __init__(self, queryset: QuerySet, date_field_name: str, start: date, end: date):
        self._queryset = queryset
        self.field = date_field_name

        now = datetime.now().date()
        if start > now or end > now or start > end:
            raise ValueError()

        self._start = start
        self._end = end

    def set_period(self, start, end):
        self._start = start
        self._end = end

    def create(self) -> Chart:
        return self.Chart(self._format_dates(self.dates), self.values)

    def _format_dates(self, dates: List[date]) -> List[str]:
        return [f"{date.day}.{date.month}" for date in dates]

    @property
    def dates(self) -> List[date]:
        return [self._start + timedelta(days=i) for i in range((self._end - self._start).days + 1)]

    @property
    def values(self) -> List[float]:
        # if self._queryset.model == Post:
        return [
            self._queryset.filter(**{self.field + "__date": date}).count()
            for date in self.dates
        ]
        # elif self._queryset.model == Comment and self.field == "count":
        #     return self._queryset.count()



