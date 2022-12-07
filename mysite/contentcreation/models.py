from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
import re

PATTERN = f'https:\/\/t.me\/\+(\w*)'


class TelegramChanelSource(models.Model):
    name = models.CharField(_('название канала'), max_length=50, unique=True)
    url = models.URLField(_('ссылка на доступ к каналу'), unique=True)
    use_in_generation = models.BooleanField(_('использовать в генерации'), default=True)

    class Meta:
        verbose_name = _('телеграм канал')
        verbose_name_plural = _('телеграм каналы')

    def clean(self):
        if len(re.findall(PATTERN, self.url)) != 1:
            raise ValidationError("Некоректный адрес")
        return super().clean()

    @property
    def formated(self):
        return "telegram.me/joinchat/{}".format(re.findall(PATTERN, self.url)[0])

    def __str__(self):
        return 'ТГ канал {}'.format(self.name)