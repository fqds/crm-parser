# app.py
from urllib import parse
from flask import Flask, request

app = Flask(__name__)

from datetime import datetime
from threading import Thread
import time

@app.route('/createdeal', methods=['POST'])
def createDealHook():
    data = parse.parse_qs(request.get_data())
    
    dealList.append({
                        "moveAt":  int(data[b'leads[add][0][date_create]'][0].decode("utf-8")), 
                        "dealID": data[b'leads[add][0][id]'][0].decode("utf-8"), 
                        "name": data[b'leads[add][0][name]'][0].decode("utf-8"),
                        "price":  data[b'leads[add][0][price]'][0].decode("utf-8"),
                        "tableCoord": [len(dealList)+1, "A"]
                    }) 
    print(dealList)
    return 'success', 200

def waitAndMove():
    while True:
        if len(dealList) != 0 and dealList[0]["moveAt"] < int(time.mktime(datetime.now().timetuple())):
            dealList[0]["moveAt"] += 30
            dealList.append(dealList.pop(0))
        else:
            time.sleep(2)

def runListener():
    app.run(host='127.0.0.1', port=8000, debug=True)
dealList = []

thread1 = Thread(target=waitAndMove).start()
runListener()


# 3) Подключиться к таблице
# 4) Изменять данные в таблице
# 5) Проверить на проде
