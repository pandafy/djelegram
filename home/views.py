from django.shortcuts import render
from pprint import pprint
# from telethon import TelegramClient
from django.conf import settings
# from .tasks import *
# from .utils import waiting_for_response
import time 
import json
from django.contrib import messages

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
    # if request.POST:
    #     if request.POST.get('submit') == 'Send Authentication Code':
    #         """ Contains logic for sending authentication code for entered number """
    #         mobile = request.POST.get('mobile')
    #         context['mobile'] = mobile
    #         response = send_code_request.delay(mobile)
    #         response = waiting_for_response(response)
    #         try:
    #             response = json.loads(response)
    #             pprint(response)
    #             context['view_code'] = True
    #             request.session['phone_code_hash'] = response['phone_code_hash']
    #             messages.success(request,"Authentication token has been successfully sent on your Telegram account.")
    #         except Exception as e:
    #             print(e)
    #             print("An error has occurred try again!")
    #             messages.error(request, "An error has occurred, please try again")
    #     else:
    #         """ Verifies authentication code entered by user"""
    #         mobile = request.POST.get('mobile')
    #         auth_code = request.POST.get('auth_code')
    #         phone_code_hash = request.session['phone_code_hash']
            
    #         response = verify_auth_code.delay(mobile,auth_code, phone_code_hash)
    #         response = waiting_for_response(response)

    #         try:
    #             response = json.loads(response)
    #             pprint(response)
    #             messages.success(request,"Authentication token has been verified, you will be redirected in a jiffy")
    #         except Exception as e:
    #             print(e, response)
    #             context['mobile'] = mobile
    #             context['view_code'] = True
    #             messages.error(request, response.split('(')[0])

    return render(request, 'home/login.html', context=context)