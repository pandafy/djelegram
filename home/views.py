from django.shortcuts import render, redirect
from django.http import JsonResponse
from pprint import pprint
import time
import json
from django.contrib import messages
from datetime import datetime
from home.custom_filters import get_item
from . import client, init
# from telethon.sync import TelegramClient
import asyncio

# loop = asyncio.get_event_loop()
entities = dict()
medias = dict()

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
                response = client.loop.run_until_complete(
                    client.send_code_request(mobile))
                pprint(response)
                context['view_code'] = True
                request.session['phone_code_hash'] = response.phone_code_hash
                messages.success(
                    request, "Authentication token has been successfully sent on your Telegram account.")
            except Exception as e:
                print(e)
                print("An error has occurred try again!")
                messages.error(
                    request, "An error has occurred, please try again")
                # client.loop.run_until_complete(client.connect())
        else:
            """ Verifies authentication code entered by user"""
            mobile = request.POST.get('mobile')
            auth_code = request.POST.get('auth_code')
            phone_code_hash = request.session['phone_code_hash']
            response = client.loop.run_until_complete(client.sign_in(
                phone=mobile, code=auth_code, phone_code_hash=phone_code_hash))
            pprint(response)
            try:
                messages.success(
                    request, "Authentication token has been verified, you will be redirected in a jiffy")
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

    if id != 0:
        try:
            entity = client.loop.run_until_complete(client.get_entity(int(id)))
            messages = client.loop.run_until_complete(
                client.get_messages(entity, limit=10))
            request.session['offset_id'] = messages[-1].id
            client.loop.run_until_complete(
                client.send_read_acknowledge(int(id), messages))
            request.session['recipient'] = int(id)
            # Use Celery task for this :P
            for message in messages[:-1]:
                if message.photo:
                    try:
                        photo_id = str(message.photo.id)
                        medias[photo_id]
                    except:
                        photo_url = client.loop.run_until_complete(
                            client.download_media(message.photo, file='media/'))
                        medias[photo_id] = photo_url
                        message.photo_id = photo_id
                        print(message.photo_id)
            context["chat_messages"] = messages
            pprint(messages)
        except Exception as e:
            print(e)
    try:

        response = client.loop.run_until_complete(client.get_dialogs())
        channels = []
        for dialog in response:
            temp = dict(name=dialog.title,
                        message=dialog.message.text,
                        id=dialog.entity.id,
                        unread_count=dialog.unread_count,
                        unread_mentions_count=dialog.unread_mentions_count,
                        entity=dialog.entity,
                        )
            temp['date'] = dialog.date.strftime('%H:%M') if dialog.date.date(
            ) == datetime.now().date() else dialog.date.strftime('%x')

            try:
                temp['sender'] = str(dialog.message.from_id)
                entities[temp['sender']]
            except:
                try:
                    entities[temp['sender']] = client.loop.run_until_complete(
                        client.get_entity(dialog.message.from_id)).first_name
                except:
                    pass

            try:
                if int(id) == temp['id']:
                    context["selected_chat"] = temp
            except Exception as e:
                print("No chat selected", e)
            channels.append(temp)

        context['channels'] = channels
    except Exception as e:
        print("asdasdasd", e)
    context['entities'] = entities
    context['medias'] = medias
    pprint(context['medias'])
    return render(request, 'home/chat.html', context=context)


def send_messages(request):
    if request.POST:
        recipient = request.POST.get('recipient')
        text = request.POST.get('text')
        if text == '':
            messages.error(request, "You can not send empty messages")
        else:
            client.loop.run_until_complete(
                client.send_message(int(recipient), message=text))
        return redirect('chat', int(recipient))


def get_more_messages(request):
    id = request.session['recipient']
    try:
        entity = client.loop.run_until_complete(client.get_entity(int(id)))
        offset_id = request.session.get('offset_id', None)
        messages = client.loop.run_until_complete(
            client.get_messages(entity, limit=10, offset_id=offset_id))
        if len(messages) == 0:
            return JsonResponse({'messages': []})
        request.session['offset_id'] = messages[-1].id
        messages_dict = []
        for message in messages[:-1]:
            message_dict = dict()
            message_dict['from_id'] = message.from_id
            print(message.text)
            if message.text:
                message_dict['text'] = message.text
            elif message.photo:
                try:
                    photo_id = str(message.photo.id)
                    medias[photo_id]
                except:
                    photo_url = client.loop.run_until_complete(
                        client.download_media(message.photo, file='media/'))
                    medias[photo_id] = photo_url

                message_dict['photo'] = medias[photo_id]
            else:
                pass
            messages_dict.append(message_dict)

        pprint(messages_dict)
    except Exception as e:
        print(e)
    return JsonResponse({'messages': messages_dict})


def logout(request):
    temp = False
    global client
    del request.session['phone_code_hash']
    request.session['phone_code_hash'] = None
    del request.session['user']
    request.session['user'] = None
    del request.session['user_id']
    request.session['user_id'] = None
    del request.session['recipient']
    request.session['recipient'] = None
    while not temp:
        try:
            temp = client.loop.run_until_complete(client.log_out())

        except ConnectionError:
            break
        except:
            pass
    init()
    print(client.loop.run_until_complete(client.connect()))

    return redirect('login')
