import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os
from datetime import datetime,date

cred = credentials.Certificate('csai-demo-firebase-adminsdk-zqtm2-4677acfdd5.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def getFile():
    folders = ['bill','challan','contractor','sale_cust','service_cust']
    day_data = ""
    if not os.path.exists("last_sync.csai"):
        with open("last_sync.csai",'a') as fp:
            fp.write("0\n0")
    with open("last_sync.csai",'r') as fp:
        day_data = fp.read()
    if id(str(day_data).strip())!=id(''):
        days = day_data.split("\n")
        seconds = int(days[1])
        days = int(days[0])
    else:
        seconds = 0
        days = 0
    try:
        for folder in folders:
            docs = db.collection(str(folder)).stream()
            if not os.path.isdir(folder):
                os.makedirs(folder)
            for doc in docs:
                filename = str(doc.id).split("\n")[0]
                data = doc.to_dict()
                if "timestamp_day" in data.keys():
                    if int(data['timestamp_day'])>=days:
                        if "timestamp_sec" in data.keys():
                            if int(data['timestamp_sec'])>=seconds:
                                with open("{}\\{}.csai".format(folder,filename),'w')as fp:
                                    json.dump(data,fp)
        d1 = date(2000,1,1)
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        seconds = (now - midnight).seconds
        days = now.date() - d1
        days = int(days.days)
        with open("last_sync.csai",'w') as fp:
            fp.write("{}\n{}".format(days,seconds))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    getFile()
