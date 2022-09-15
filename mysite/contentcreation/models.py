from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramChanelSource(models.Model):
    name = models.CharField(_('название канала'), max_length=50, unique=True)
    url = models.URLField(_('ссылка на доступ к каналу'), unique=True)

    class Meta:
        verbose_name = _('телеграм канал')
        verbose_name_plural = _('телеграм каналы')

    def __str__(self):
        return 'ТГ канал {}'.format(self.name)