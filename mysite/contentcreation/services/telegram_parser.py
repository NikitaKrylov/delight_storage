from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
from mysite.settings import MEDIA_ROOT
from random import choice

api_id = '17810821'
api_hash = '742ceea4305ac925a1ebb092015dfe39'
username = 'grabber'
channel_url = 'https://t.me/joinchat/UeveaXzmViPhTd2c'
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient(username, api_id, api_hash, loop=loop)
client.start()


class TelegramParser:

    async def get_random_image(self, channel_url:str, limit=20) -> str:
        history = await self._get_history(channel_url, limit=limit)
        target_messages = []
        for message in history.messages:
            if message.media is not None:
                target_messages.append(message)

        path = await client.download_media(choice(target_messages), MEDIA_ROOT + 'images')
        return path

    async def _get_channel(self, url):
        return await client.get_entity(channel_url)

    async def _get_history(self, url, limit=20):
        channel = await self._get_channel(url)
        return await client(GetHistoryRequest(
        peer=channel,
        offset_date=None, add_offset=0,
        offset_id=0,
        limit=limit, max_id=0, min_id=0,
        hash=0))





