import time
from  telethon import TelegramClient
from django.conf import settings

async def send_code_request(mobile):
    client = TelegramClient('session_namea', settings.API_ID, settings.API_HASH)
    await client.connect()
    try: 
        response = await client.send_code_request(phone=mobile)
        return response.to_json()
    except Exception as e:
        return str(e)

async def sign_in(mobile, code, phone_code_hash):
    client = TelegramClient('session_namea', settings.API_ID, settings.API_HASH)
    await client.connect()
    try: 
        response = await client.sign_in(phone=mobile, code=code, phone_code_hash=phone_code_hash)
        return response.to_json()
    except Exception as e:
        return str(e)


def waiting_for_response(response):
    while not response.ready():
        time.sleep(1)
    return response.result
            