from flask import Flask, request
from api.crawler.menu import mensaMenuAsJson

app = Flask(__name__)

@app.route('/')
def home():
    return 'Make a menu request to /menu?date=YYYY-MM-DD&location=LOCATION'

@app.route('/menu', methods=['GET'])
def menu():
    args=request.args
    args=args.to_dict()
    return mensaMenuAsJson(args.get('date'), args.get('location'))