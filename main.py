# app.py
import os
from urllib import parse
from flask import Flask, request
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from threading import Thread
import time

dealList = []
app = Flask(__name__)

@app.route('/createdeal', methods=['POST'])
def createDealHook():
    data = parse.parse_qs(request.get_data())
    
    print(data[b'leads[add][0][id]'][0].decode("utf-8"), data[b'leads[add][0][name]'][0].decode("utf-8"), data[b'leads[add][0][price]'][0].decode("utf-8") )

    dealList.append({
                        "moveAt":  int(data[b'leads[add][0][date_create]'][0].decode("utf-8")), 
                        "dealID": data[b'leads[add][0][id]'][0].decode("utf-8"), 
                        "name": data[b'leads[add][0][name]'][0].decode("utf-8"),
                        "price":  data[b'leads[add][0][price]'][0].decode("utf-8"),
                        "tableCoord": ["A", len(dealList)+1]
                    }) 
    SERVICE.spreadsheets().values().batchUpdate(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f"{dealList[0]['tableCoord'][0]}{dealList[0]['tableCoord'][1]}:{dealList[0]['tableCoord'][0]}{dealList[0]['tableCoord'][1]}",
                "majorDimension": "ROWS",
                "values": [[dealList[0]['dealID'] + "\n" + dealList[0]['name'] + "\n" + dealList[0]['price']]]
                }
            ]
        }
    ).execute()
    print(dealList)
    return 'success', 200
    

def waitAndMove():
    while True:
        if dealList and dealList[0]["moveAt"] < int(time.mktime(datetime.now().timetuple())):
            SERVICE.spreadsheets().values().batchUpdate(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": f"{dealList[0]['tableCoord'][0]}{dealList[0]['tableCoord'][1]}:{getHigherCharacter(dealList[0]['tableCoord'][0])}{dealList[0]['tableCoord'][1]}",
                        "majorDimension": "ROWS",
                        "values": [["", dealList[0]['dealID'] + "\n" + dealList[0]['name'] + "\n" + dealList[0]['price']]]
                        }
                    ]
                }
            ).execute()
            dealList[0]["moveAt"] += 20
            dealList[0]["tableCoord"][0] = getHigherCharacter(dealList[0]["tableCoord"][0])
            dealList.append(dealList.pop(0))
            time.sleep(1)
        else:
            time.sleep(0.5)

def getHigherCharacter(character):
    if character[-1] == "Z":
        if len(character) == 1: return "AA"
        return getHigherCharacter(character[:-1]) + "A"
    return character[:-1] + chr(ord(character[-1]) + 1)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.path.join(os.curdir, "credentials.json")
CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = '156Ug6eEEdmcoQMllCw7tww6sh6Ofwx9ORP0qMLcXkVM'
SERVICE = build('sheets', 'v4', credentials=CREDENTIALS)

def main():
    Thread(target=waitAndMove).start()
    app.run(host='185.211.170.140', port=8000, debug=True)

if __name__ == '__main__':
    main()
