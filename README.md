# Intro

This is a POC Django app using Telegram for authentication.

# Quickstart

Clone this repo and then:-

    cd gramlogin
    heroku create
    heroku config:set BOT_TOKEN=<Your telegram bot token> BOT_WHTOKEN=<secret token for webhook url>

This app now created on heroku. Let set the webhook url:-

    python3.6 -mvenv venv
    venv/bin/python/pip install -r requirements.txt
    venv/bin/python set_webhook.py <heroku url> <telegram-bot-token> <webhook-token>

We can push this to heroku:-

    git push heroku master

## License: MIT

## Further Reading

- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
