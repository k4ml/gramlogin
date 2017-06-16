#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gramlogin.settings")
    url = sys.argv[1]
    bot_token = sys.argv[2]
    bot_whtoken = sys.argv[3]

    from telegram.ext import Updater
    updater = Updater(bot_token)
    updater.bot.set_webhook(url + bot_whtoken + '/')
