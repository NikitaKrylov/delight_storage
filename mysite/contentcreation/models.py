from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramChanelSource(models.Model):
    name = models.CharField(_('название канала'), max_length=50)
    url = models.URLField(_('ссылка на доступ к каналу'))