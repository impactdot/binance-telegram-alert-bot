from flask import Flask, render_template, request

import os
import telegram

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def webhook():
    bot = telegram.Bot(token=os.environ["YOURAPIKEY"])
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.effective_chat.id
        text = update.message.text
        first_name = update.effective_chat.first_name
        # Reply with the same message
        bot.sendMessage(chat_id=chat_id, text=f"{text} {first_name}")
        return "ok"
    return "error"


def index():
    return webhook()


# https://api.telegram.org/bot5822639543:AAFvPYODp9nmX6_mbYLxr_K7F5FyumLuqcQ/setWebhook?url=https://binance-telegram-alert-bot.herokuapp.com/
#
