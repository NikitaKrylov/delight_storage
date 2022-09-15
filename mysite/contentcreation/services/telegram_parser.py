from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
from mysite.settings import MEDIA_ROOT
from random import choice

api_id = '17810821'
api_hash = '742ceea4305ac925a1ebb092015dfe39'
username = 'grabber'
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def get_random_image(channel_url: str, limit=50) -> str:
    async with TelegramClient(username, api_id, api_hash, loop=loop) as client:
        history = await _get_history(client, channel_url, limit=limit)
        target_messages = []
        for message in history.messages:
            if message.photo:
                target_messages.append(message)

        path = await client.download_media(choice(target_messages).photo, MEDIA_ROOT + 'images')
        return path


async def _get_channel(client, url):
    return await client.get_entity(url)


async def _get_history(client, url, limit=50):
    channel = await _get_channel(client, url)
    return await client(GetHistoryRequest(
    peer=channel,
    offset_date=None, add_offset=0,
    offset_id=0,
    limit=limit, max_id=0, min_id=0,
    hash=0))




