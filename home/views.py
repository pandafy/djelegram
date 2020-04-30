from django.shortcuts import render, redirect
from pprint import pprint
from telethon import TelegramClient
from django.conf import settings
from .tasks import *
from .utils import waiting_for_response, send_code_request
import time 
import json
from django.contrib import messages
# from telethon.sync import TelegramClient


client =  TelegramClient('asd',settings.API_ID, settings.API_HASH)
client.loop.run_until_complete(client.connect())
loop = asyncio.get_event_loop()

# Create your views here.

def home(request):
    """
    Renders homepage for our application
    """

    return render(request, 'home/index.html')

def login(request):
    context = dict()
    """
    Renders and handles login page
    """
    if request.POST:
        if request.POST.get('submit') == 'Send Authentication Code':
            """ Contains logic for sending authentication code for entered number """
            mobile = request.POST.get('mobile')
            context['mobile'] = mobile
            try:
                response = client.loop.run_until_complete(client.send_code_request(mobile))
                pprint(response)
                context['view_code'] = True
                request.session['phone_code_hash'] = response.phone_code_hash
                messages.success(request,"Authentication token has been successfully sent on your Telegram account.")
            except Exception as e:
                print(e)
                print("An error has occurred try again!")
                messages.error(request, "An error has occurred, please try again")
        else:
            """ Verifies authentication code entered by user"""
            mobile = request.POST.get('mobile')
            auth_code = request.POST.get('auth_code')
            phone_code_hash = request.session['phone_code_hash']
            response = client.loop.run_until_complete(client.sign_in(phone=mobile, code=auth_code,phone_code_hash=phone_code_hash   ))
            pprint(response)
            try:
                messages.success(request,"Authentication token has been verified, you will be redirected in a jiffy")
                request.session['user'] = response.to_json()
                return redirect('chat')
            except Exception as e:
                print(e, response)
                context['mobile'] = mobile
                context['view_code'] = True
                messages.error(request, response.split('(')[0])

    return render(request, 'home/login.html', context=context)


def chat(request, id=None):
    """
    Renders and handles chat page
    """
    context = dict()

    if request.POST:
        pass
    response = client.loop.run_until_complete(client.get_dialogs())
    for dialog in response:
        print(dialog.title, dialog.message.text, str(dialog.date))
    return render(request, 'home/chat.html', context=context)