#!python3
import flask
import random
import string
from flask import Flask
from flask import request
from datetime import datetime
from ua_parser import user_agent_parser

app = Flask(__name__)


@app.route("/random")
def search():
    args = request.args

    length = int(args.get('length'))
    specials = int(args.get('specials', 0))
    digits = int(args.get('digits', 0))
    if 0 < length < 101:
        if specials == 1 and digits == 1:
            punct = string.punctuation
            digi = string.digits
        elif specials == 0 and digits == 1:
            punct = ''
            digi = string.digits
        elif specials == 1 and digits == 0:
            punct = string.punctuation
            digi = ''
        elif specials == 0 and digits == 0:
            punct = ''
            digi = ''
        elif specials != 0 and specials != 1 and digits not in (0, 1):
            return "<p>Please input specials 0 or 1 </p>" \
                   "<p>Please input digits 0 or 1 </p>"
        elif specials != 0 and specials != 1 and digits in (0, 1):
            return "<p>Please input specials 0 or 1 </p>"
        elif digits != 0 and digits != 1:
            return "<p>Please input digits 0 or 1 </p>"
        characters = string.ascii_letters + punct + digi
        result_str = ''.join(random.choice(characters) for i in range(length))
        if len(result_str) == length:
            return f"<p>Random string: {result_str}</p>"
    else:
        if specials in (0,1) and digits in (0, 1):
            return "<p>Please, input length in range from 1 to 100</p>"
        elif specials != 0 and specials != 1 and digits in (0, 1):
            return "<p>Please, input length in range from 1 to 100</p>"\
                   "<p>Please, input specials 0 or 1 </p>"
        elif specials not in (0, 1) and digits not in (0, 1):
            return "<p>Please, input length in range from 1 to 100</p>" \
                   "<p>Please, input specials 0 or 1 </p>"\
                   "<p>Please, input digits 0 or 1 </p>"


@app.route("/whoami")
def index():
    ip_address = flask.request.remote_addr
    now = datetime.now().strftime('%H:%M:%S  date %d-%m-%y')
    browser = user_agent_parser.Parse(request.user_agent.string)['user_agent']['family']
    return f'Browser: {browser}' \
        f'<p>Requester IP:  {ip_address} </p>' + \
        f' Current time: {now}'


@app.route("/source_code")
def code():
    return open(__file__).readlines()


if __name__ == '__main__':
    app.run(debug=True)
