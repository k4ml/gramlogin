
import os
import json
import pprint

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.core.signing import TimestampSigner
from django.contrib.auth.decorators import login_required

import telegram

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_WHTOKEN = os.environ['BOT_WHTOKEN']
bot = telegram.Bot(token=BOT_TOKEN)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

@login_required(login_url='/login/')
def index(request):
    return HttpResponse('hello %s' % request.user.username)

def login(request):
    auths = request.GET.get('auths', None) or request.POST.get('auths', None)
    if auths is None:
        return HttpResponseForbidden()

    if request.method == 'POST':
        user = authenticate(request, auths=auths)
        if user is None:
            return render(request, 'login.html', context={"message": "Login Fail"})
        else:
            auth_login(request, user)
            return redirect(index)

    return render(request, 'login.html', context={'auths': auths})

@csrf_exempt
def handle_bot(request, token):
    if token != BOT_WHTOKEN:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        print(json.dumps(data, indent=4))
        update = telegram.Update.de_json(data, bot)
        print(update.message.chat.id, update.message.chat.username, update.message.text)
        chat_id = update.message.chat.id
        username = update.message.chat.username
        first_name = update.message.chat.first_name
        username = username or first_name
        signer = TimestampSigner()
        auths = signer.sign(username)
        login_url = request.build_absolute_uri('/login/') + '?auths=%s' % auths
        button_list = [
            telegram.InlineKeyboardButton("Login", url=login_url),
        ]
        reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        bot.sendMessage(chat_id=chat_id, text="Click the button below to login. It only valid for 2 minutes. After that, you have to type 'Login' again.", reply_markup=reply_markup)
    return HttpResponse()
