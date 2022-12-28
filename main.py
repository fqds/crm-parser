# app.py
import json
from urllib import parse
from flask import Flask, request

app = Flask(__name__)

@app.route('/createdeal', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(parse.parse_qs(request.get_data()))
        return 'success', 200
    else:
        abort(400)



app.run(host='185.211.170.140', port=8000, debug=True)
