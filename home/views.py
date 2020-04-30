from django.shortcuts import render, redirect
from pprint import pprint
from telethon import TelegramClient
from django.conf import settings
from .tasks import *
from .utils import waiting_for_response, send_code_request
import time 
import json
from django.contrib import messages
from datetime import datetime
from home.custom_filters import get_item
# from telethon.sync import TelegramClient


client =  TelegramClient('asd',settings.API_ID, settings.API_HASH)
client.loop.run_until_complete(client.connect())
loop = asyncio.get_event_loop()
entities = dict()

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
                request.session['user_id'] = response.id
                return redirect('chat')
            except Exception as e:
                print(e, response)
                context['mobile'] = mobile
                context['view_code'] = True
                messages.error(request, response.split('(')[0])

    return render(request, 'home/login.html', context=context)


def chat(request, id=0):
    """
    Renders and handles chat page
    """
    context = dict()
    if request.session.get('user_id', None) == None:
        return redirect('login')
    if request.POST:
        pass

    if id:
        try:
            entity = client.loop.run_until_complete(client.get_entity(int(id)))
            messages = client.loop.run_until_complete(client.get_messages(entity, limit=20))
            context["messages"] = messages
            request.session['recipient'] = int(id)
            # Use Celery task for this :P
            # for message in messages[:-1]:
            #     client.loop.run_until_complete(message.mark_read())
        except Exception as e:
            pprint(e)
    try:

        response = client.loop.run_until_complete(client.get_dialogs())
        channels = []
        for dialog in response:
            temp = dict(name=dialog.title, 
                                message = dialog.message.text,
                                id = dialog.entity.id,
                                unread_count= dialog.unread_count,
                                unread_mentions_count= dialog.unread_mentions_count,
                                entity=dialog.entity,                                
                                )
            temp['date'] = dialog.date.strftime('%H:%M') if dialog.date.date() == datetime.now().date() else dialog.date.strftime('%x')

            try:
                temp['sender'] = str(dialog.message.from_id)
                entities[temp['sender']]
            except:
                try:
                    entities[temp['sender']] =client.loop.run_until_complete(client.get_entity(dialog.message.from_id)).first_name
                except:
                    pass
            

            try:
                if int(id) == temp['id']:
                    context["selected_chat"] = temp
            except Exception as e:
                pprint("No chat selected", e)
            channels.append(temp)

        context['channels'] = channels
    except Exception as e:
        pprint("asdasdasd",e)
    context['entities'] = entities
    return render(request, 'home/chat.html', context=context)

def send_messages(request):
    if request.POST:
        recipient = request.POST.get('recipient')
        text = request.POST.get('text')
        client.loop.run_until_complete(client.send_message(int(recipient),message=text))
        return redirect('chat', int(recipient))

def logout(request):
    temp = False
    while not temp:
        temp = client.loop.run_until_complete(client.log_out())
        del request.session['phone_code_hash']
        del request.session['user']
        del request.session['user_id']
        del request.session['recipient']
    client.loop.run_until_complete(client.connect())

    return redirect('login')