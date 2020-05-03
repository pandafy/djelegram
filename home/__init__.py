from telethon import TelegramClient
from django.conf import settings
import asyncio

client = None


def init():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    global client
    client = TelegramClient('asd', settings.API_ID, settings.API_HASH)
    client.loop.run_until_complete(client.connect())
    client = client
    return client


init()
