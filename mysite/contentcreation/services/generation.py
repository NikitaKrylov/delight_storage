from random import choice

from django.core.files import File

from .telegram_parser import loop, get_random_image
from ..models import TelegramChanelSource
import os

api_id = '17810821'
api_hash = '742ceea4305ac925a1ebb092015dfe39'
username = 'grabber'


class ContentGenerator:
    def generate(self) -> str:
        return self._from_telegram()

    def _from_telegram(self):
        url = choice(TelegramChanelSource.objects.values_list('url'))
        path = loop.run_until_complete(get_random_image(url[0]))
        return 'images/' + os.path.basename(path)

