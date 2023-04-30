from django.test import TestCase

from mediacore.models import ImageFile
from .models import TelegramChanelSource
from .services.generation import ContentParser
# Create your tests here.


class ParserTestCase(TestCase):
    def setUp(self):
        TelegramChanelSource.objects.create(url="https://t.me/+YiOprFrvB5U2YmFi")

    def is_func_starts(self):
        parser = ContentParser()

        for _ in range(10):
            self.assertIs(parser.get(lazy=True), str)

        for _ in range(10):
            self.assertIs(parser.get(), ImageFile)
