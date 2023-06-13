import flask
from flask import request, jsonify
from api.crawler.menu import mensaMenuAsJson
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

app = flask.Flask(__name__)

bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'), threaded=False)
bot.remove_webhook()
bot.set_webhook(url="https://unigoemensaplan.vercel.app/webhook")

@app.route('/')
def home():
    return 'Make a menu request to /menu?date=YYYY-MM-DD&location=LOCATION'

@app.route("/webhook", methods=["POST"])
def webhook():
    if flask.request.headers.get("content-type") == "application/json":
        json_string = flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        flask.process_new_updates([update])
        return ""
    else:
        app.abort(403)


@app.route('/menu', methods=['GET'])
def menu():
    args=request.args
    args=args.to_dict()
    return jsonify(mensaMenuAsJson(args.get('date'), args.get('location')))

# Handle '/start' and '/help'
@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(
        message,
        """
        Welcome to the demo bot. 

        Send a message to get an echo reply

        /gpt <message> - Get a GPT-3 generated reply based on your prompt in gpt.py
        
        """,
    )
