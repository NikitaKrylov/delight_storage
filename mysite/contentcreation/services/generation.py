from random import choice
from .telegram_parser import loop, get_random_image
from ..models import TelegramChanelSource
from mysite.settings import POST_MEDIA_PATH
import os

api_id = '17810821'
api_hash = '742ceea4305ac925a1ebb092015dfe39'
username = 'grabber'


class ContentGenerator:
    last_source_type: str = None
    last_source_name: str = None

    def generate(self) -> str:
        return self._from_telegram()

    def _from_telegram(self):
        self.last_source_type = TelegramChanelSource._meta.verbose_name_plural.title()
        url, name = choice(TelegramChanelSource.objects.values_list('url', 'name'))
        self.last_source_name = name
        path = loop.run_until_complete(get_random_image(url))
        return POST_MEDIA_PATH + '/' + os.path.basename(path)


