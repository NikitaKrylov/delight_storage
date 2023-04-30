from random import choice
from typing import Union

from asgiref.sync import async_to_sync

from django.core.files.images import ImageFile as file
from mediacore.models import ImageFile
from .telegram_parser import get_random_image
from ..models import TelegramChanelSource
from mysite.settings import POST_MEDIA_PATH
import os

api_id = '17810821'
api_hash = '742ceea4305ac925a1ebb092015dfe39'
username = 'grabber'


class ContentParser:
    last_source_type: str = None
    last_source_name: str = None

    def get(self, lazy=False) -> Union[str, ImageFile]:
        path = self._from_telegram()
        if lazy:
            return path
        return self.create_image_file(path)

    def _from_telegram(self):
        self.last_source_type = TelegramChanelSource._meta.verbose_name_plural.title()
        source = choice(TelegramChanelSource.objects.filter(use_in_generation=True))
        self.last_source_name = source.name
        path = async_to_sync(get_random_image)(source.formated)
        print(path)
        return POST_MEDIA_PATH + '/' + os.path.basename(path)

    @staticmethod
    def create_image_file(path, **kwargs):
        return ImageFile.objects.create(file=path, **kwargs)


