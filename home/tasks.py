# from celery import shared_task
# from  telethon import TelegramClient
# from django.conf import settings    
# import asyncio
# from . import utils


# @shared_task
# def send_code_request(mobile):
#    return asyncio.run(utils.send_code_request(mobile))
   
# @shared_task
# def verify_auth_code(mobile, code, phone_code_hash):
#     return asyncio.run(utils.sign_in(mobile, code, phone_code_hash))