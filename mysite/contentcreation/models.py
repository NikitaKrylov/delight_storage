from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import re


class TelegramChanelSource(models.Model):
    name = models.CharField(_('название канала'), max_length=50, unique=True)
    url = models.URLField(_('ссылка на доступ к каналу'), unique=True)
    use_in_generation = models.BooleanField(_('использовать в генерации'), default=True)

    class Meta:
        verbose_name = _('телеграм канал')
        verbose_name_plural = _('телеграм каналы')

    @property
    def formated(self):
        if self.url.find('+') != -1:
            return "https://t.me/joinchat/{}".format(re.findall(f"https:\/\/t.me\/\+(\w*)", self.url)[0])
        return self.url

    def __str__(self):
        return 'ТГ канал {}'.format(self.name)