import flask
from flask import request, jsonify
from api.crawler.menu import mensaMenuAsJson
import os
import telebot
from dotenv import load_dotenv

load_dotenv()

app = flask.Flask(__name__)

bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'), threaded=False)


@app.route('/')
def hello():
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
    return jsonify(mensaMenuAsJson(args.get('date'), args.get('location')))

# Handle '/start' and '/help'
@bot.message_handler(commands=["mensa"])
def send_welcome(message):
    menu = mensaMenuAsJson('2023-06-13', 'zentralmensa')

    reply = "Heute in der Zentralmensa gibt es:\n\n"
    reply += "Ort: " + menu['location'] + "\n"
    reply += "Datum: " + menu['date'] + "\n\n"
    for meal in menu['meals']:
      reply += meal['type'] + ": " + meal['name'] + "\n"
      reply += "Zutaten: " + meal['meal_ingredients'] + "\n"
    if meal['content'] != '':
      reply += "Angebot: " + meal['content'] + "\n"
      reply += "\n"

    bot.reply_to(
        message,reply
    )


#if __name__ == "__main__":
#    # Remove webhook, it fails sometimes the set if there is a previous webhook
#    bot.remove_webhook()
#    #bot.set_webhook(url="https://unigoemensaplan.vercel.app/webhook")
#    bot.set_webhook(url="https://3409-2a01-c22-8442-3500-b5a7-2e07-c70-347.ngrok-free.app/webhook")