import flask
from flask import request, jsonify
from api.crawler.meals import mensa_meals_as_dict
from api.bot.meals_reply import bot_meals_reply
import requests

import os
import telebot
from dotenv import load_dotenv
import datetime
from zoneinfo import ZoneInfo



load_dotenv()

app = flask.Flask(__name__)

bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'), threaded=False)


@app.route('/')
def hello():
    return {"status": "ok"}

@app.route('/renew_webhook')
def renew_webhook():
    response = requests.get(f"https://api.telegram.org/bot{os.environ.get('TELEGRAM_TOKEN')}/setWebhook?url=https://unigoemensaplan.vercel.app/webhook")
    if response.status_code == 400:
        return {"status": "error"}
    else:
        return {"status": "ok"}

@app.route("/webhook", methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        app.abort(403)


@app.route('/menu', methods=['GET'])
def menu():
    args=request.args
    args=args.to_dict()
    return jsonify(mensa_meals_as_dict(args.get('date'), args.get('location')))

# Bot routes from here on
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,"Willkommen beim Mensa Bot!\n\nWähle im Menü unten links eine Mensa aus, von der du das Menü für heute sehen willst. \nDieser Bot steht in keiner Verbindung zur Uni Göttingen.",parse_mode='Markdown'
    )
    return

@bot.message_handler(commands=["zentralmensa","mensaamturm","lunchbox"])
def send_mensa(message):
    #Get the command from the message
    command = message.text.split(" ")[0]
    if command == "/zentralmensa":
        location = "zentralmensa"
    elif command == "/mensaamturm":
        location = "mensa_am_turm"
    elif command == "/lunchbox":
        location = "lunchbox"
    else:
        bot.reply_to(
        message,"Wähle eine Mensa aus",parse_mode='Markdown'
    )
        return
    

    current_date = datetime.datetime.now(tz=ZoneInfo("Europe/Berlin"))
    meals = mensa_meals_as_dict(current_date.strftime("%Y-%m-%d"), location)
    reply = bot_meals_reply(meals)
    bot.reply_to(
        message,reply,parse_mode='Markdown'
    )
    return


#if __name__ == "__main__":
#    # Remove webhook, it fails sometimes the set if there is a previous webhook
#    bot.remove_webhook()
#    #bot.set_webhook(url="https://unigoemensaplan.vercel.app/webhook")
#    bot.set_webhook(url="https://3409-2a01-c22-8442-3500-b5a7-2e07-c70-347.ngrok-free.app/webhook")


# Set a webhook https://api.telegram.org/bot<Your Bot Token>/setWebhook?url=<URL that you got from Vercel>