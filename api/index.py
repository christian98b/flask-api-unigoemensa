from flask import Flask, request, jsonify
from api.crawler.menu import mensaMenuAsJson
import os
import telebot

app = Flask(__name__)

bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'), threaded=False)

@app.route('/')
def home():
    return 'Make a menu request to /menu?date=YYYY-MM-DD&location=LOCATION'

@app.route("/webhook", methods=["POST"])
def webhook():
    if Flask.request.headers.get("content-type") == "application/json":
        json_string = Flask.request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ""
    else:
        Flask.abort(403)


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

if __name__ == "__main__":
    # Remove webhook, it fails sometimes the set if there is a previous webhook
    bot.remove_webhook()
    bot.set_webhook(url="https://unigoemensaplan.vercel.app/webhook")