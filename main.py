# app.py
from urllib import parse
from flask import Flask, request
from google.oauth2 import service_account

app = Flask(__name__)

from datetime import datetime
from threading import Thread
import time

@app.route('/createdeal', methods=['POST'])
def createDealHook():
    data = parse.parse_qs(request.get_data())
    data = {b'leads[add][0][id]': [b'1190401'], b'leads[add][0][name]': [b'AASDASD'], b'leads[add][0][status_id]': [b'53861254'], b'leads[add][0][price]': [b'34343'], b'leads[add][0][responsible_user_id]': [b'9040358'], b'leads[add][0][last_modified]': [b'1672189247'], b'leads[add][0][modified_user_id]': [b'9040358'], b'leads[add][0][created_user_id]': [b'9040358'], b'leads[add][0][date_create]': [b'1672189247'], b'leads[add][0][pipeline_id]': [b'6254262'], b'leads[add][0][account_id]': [b'30739638'], b'leads[add][0][created_at]': [b'1672189247'], b'leads[add][0][updated_at]': [b'1672189247'], b'account[subdomain]': [b'121273hvv'], b'account[id]': [b'30739638'], b'account[_links][self]': [b'https://121273hvv.amocrm.ru']}
    
    print(data[b'leads[add][0][id]'][0].decode("utf-8") + "\n" + data[b'leads[add][0][name]'][0].decode("utf-8") + "\n" + data[b'leads[add][0][price]'][0].decode("utf-8") )

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
        print("\n\n\n\n\n\n\n\n")
        print(dealList)
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

# Настройки GoggleAPI
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = BASE_DIR / 'static/credentials.json'
CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = '156Ug6eEEdmcoQMllCw7tww6sh6Ofwx9ORP0qMLcXkVM'

# 3) Подключиться к таблице
# 4) Изменять данные в таблице
# 5) Проверить на проде
