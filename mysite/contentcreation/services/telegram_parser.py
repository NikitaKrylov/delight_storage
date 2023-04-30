from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio
from mysite.settings import MEDIA_ROOT, POST_MEDIA_PATH
from random import choice
import os
from mysite.settings import API_ID, API_HASH, USERNAME


async def get_random_image(channel_url: str, limit=80) -> str:
    async with TelegramClient(USERNAME, API_ID, API_HASH) as client:
        history = await _get_history(client, channel_url, limit=limit)
        target_messages = []
        for message in history.messages:
            if message.photo:
                target_messages.append(message)

        if not os.path.exists(MEDIA_ROOT + POST_MEDIA_PATH):
            os.makedirs(MEDIA_ROOT + POST_MEDIA_PATH)
        path = await client.download_media(choice(target_messages).photo, MEDIA_ROOT + POST_MEDIA_PATH)
        return path


async def _get_channel(client, url):
    return await client.get_entity(url)


async def _get_history(client, url, limit=80):
    channel = await _get_channel(client, url)
    return await client(GetHistoryRequest(
    peer=channel,
    offset_date=None, add_offset=0,
    offset_id=0,
    limit=limit, max_id=0, min_id=0,
    hash=0))




