
import os
import json
import pprint

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

import telegram

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_WHTOKEN = os.environ['BOT_WHTOKEN']
bot = telegram.Bot(token=BOT_TOKEN)

def login(request):
    return HttpResponse('hello')

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
        bot.sendMessage(chat_id=chat_id, text="ECHO: %s" % update.message.text)
    return HttpResponse()
