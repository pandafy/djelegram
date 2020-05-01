from telethon import TelegramClient
from django.conf import settings

client = None

def init():
    global client
    client =  TelegramClient('asd',settings.API_ID, settings.API_HASH)
    client.loop.run_until_complete(client.connect())
    client = client
    return client

init()
