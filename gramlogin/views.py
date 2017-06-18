
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
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import telegram

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_WHTOKEN = os.environ['BOT_WHTOKEN']
bot = telegram.Bot(token=BOT_TOKEN)
signer = TimestampSigner()

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
    auths = signer.sign('logout')
    context = {
                'logout_url': reverse('logout') + '?auths=%s' % auths,
            }
    return render(request, 'index.html', context)

def login(request):
    auths = request.GET.get('auths', None) or request.POST.get('auths', None)
    if auths is None:
        return render(request, 'login.html')

    if request.method == 'POST':
        user = authenticate(request, auths=auths)
        if user is None:
            return render(request, 'login.html', context={"message": "Login Fail"})
        else:
            auth_login(request, user)
            return redirect(index)

    username = auths.split(':')[0]
    return render(request, 'login.html', context={'auths': auths,'username': username})

@login_required(login_url='/login/')
def logout(request):
    try:
        auths = signer.unsign(request.GET.get('auths', ''))
    except Exception as e:
        print(e)
        return redirect(index)

    auth_logout(request)
    return redirect(login)

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
        if not username:
            tg_faq = 'https://telegram.org/faq#usernames-and-t-me'
            bot.sendMessage(chat_id=chat_id, text='To login with Telegram, you must create a username. Refer %s for details.' % tg_faq)
            return HttpResponse()

        auths = signer.sign(username)

        user, created = User.objects.get_or_create(username=username)

        login_url = request.build_absolute_uri('/login/') + '?auths=%s' % auths
        button_list = [
            telegram.InlineKeyboardButton("Login", url=login_url),
        ]
        reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
        bot.sendMessage(chat_id=chat_id, text="Click the button below to login. It only valid for 2 minutes. After that, you have to type 'Login' again.", reply_markup=reply_markup)
    return HttpResponse()
