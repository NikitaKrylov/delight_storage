from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from notifications.base.models import AbstractNotification


COMPLAINT_TYPES = (
    ('TAG_M', 'Несоответствие тегу'),
    ('AUTHOR_M', 'Несоответствие тегу'),
    ('BAD_QUALITY', 'Плохое качество'),
    ('ERROR', 'Ошибка сайта'),
    ('IRREL_CONTENT', 'Несоответствующий контент'),
)

COMPLAINT_STATUS = (
    ('ADOPTED', 'Принята'),
    ('REJECTED', "Отклонена"),
    ('IS_PENDING', 'В рассмотрении'),
)


class Complaint(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(verbose_name=_("тип жалобы"), choices=COMPLAINT_TYPES, max_length=20)
    comment = models.TextField(_('описание'), max_length=200)
    status = models.CharField(verbose_name=_("статус"), choices=COMPLAINT_STATUS, default="IS_PENDING", max_length=20)
    creation_date = models.DateTimeField(verbose_name=_('дата создания'), auto_now_add=True, editable=False)
    url = models.URLField(_('место ошибки'), blank=True, null=True)

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        return "{author_name} -> {type} | {status}".format(type=self.type, author_name=self.author.username, status=self.status)


